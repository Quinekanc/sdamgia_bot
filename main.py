import os

from DBmodels.User import User

vipshome = os.path.abspath(os.getcwd()) + '\\vips\\vips-dev-8.12\\bin\\'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']

from DBmodels.Task import Task
from models.TaskModel import TaskModel
from enums.LogLevel import LogLevel
from sdamgia import SdamGIA
import interactions
from interactions.api.models.misc import MISSING
from utils.Log import log, InitLogger
from DBmodels import DbConnection
import json
from data import Subjects
from DBmodels.Classes import Class
from models.SdamGiaResponse import *
import discord
from utils.ImageUtils import GetPng, InitImageUtils



with open("token.txt", mode='r', encoding='utf8') as f:
    TOKEN = f.read()

with open("guildIDs.json", mode='r', encoding='utf8') as f:
    data = json.loads(f.read())
    if len(data['ids']) == 0:
        GuildIDS = MISSING
    else:
        GuildIDS = data['ids']


bot = interactions.Client(token=TOKEN, intents=interactions.Intents.ALL, disable_sync=True)

sdamgia = SdamGIA()
InitLogger(LogLevel.INFO)
InitImageUtils()
DbConnection.InitDb("db.sqlite")

TaskCache = {}


@bot.event
async def on_ready():
    log(f"Logged into {bot.me.name}", loglevel=LogLevel.INFO)


@bot.command(
    name="status",
    description="Статус бота",
    scope=GuildIDS
)
async def StatusCommand(ctx: interactions.CommandContext):
    emb = interactions.Embed(title="Статус бота",
                             description=f"`Ping={bot.latency}ms`",
                             color=0xff00)

    await ctx.send(embeds=[emb])


async def FindTask(subject: str, number: int, ctx):
    try:
        result = TaskModel(sdamgia.get_problem_by_id(subject, str(number)), ctx.author, subject)
    except Exception as ex:
        log(ex, loglevel=LogLevel.ERROR)
        await ctx.send("Произошла ошибка")
        return

    if result is None:
        await ctx.send("Задание не найдено", ephemeral=True)
        return

    TaskCache[result.uuid] = result

    db = DbConnection.CreateSession()
    task = Task()
    task.Id = result.uuid
    task.TaskId = result.id
    task.ClassTaskId = None
    task.SubjectId = subject
    task.StudentId = int(ctx.author.id)

    db.add(task)
    db.commit()

    if len(result.condition.images) == 0:
        embs = [interactions.Embed(title=f"Задание №{number}",
                                   description=f"""`{result.condition.text}`""",
                                   color=0xff00)]
    else:
        await ctx.defer()
        embs = []
        for imgUrl in result.condition.images:
            img = GetPng(imgUrl)
            emb = discord.Embed(title=f"Задание №{number}",
                                description=f"""`{result.condition.text}`""",
                                color=0xff00,
                                url=result.url)
            emb.set_image(url=img)
            embs.append(interactions.Embed(**emb.to_dict()))

    await ctx.send(embeds=embs,
                   components=[
                       interactions.Button(style=interactions.ButtonStyle.SUCCESS,
                                           label="Ответить",
                                           custom_id=f"SolveTask_{result.uuid}")
                   ])


@bot.command(
    name="task",
    description="Получить задание",
    scope=GuildIDS,
    options=[
        interactions.Option(
            name="find",
            description="Найти задание по номеру и предмету",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                    name="subject",
                    description="Предмет",
                    type=interactions.OptionType.STRING,
                    required=True,
                    choices=Subjects.subjects
                ),
                interactions.Option(
                    name="number",
                    description="Номер задания",
                    type=interactions.OptionType.INTEGER,
                    required=True
                )
            ]
        ),
        interactions.Option(
            name="give",
            description="Выдать задание с номером и предметом",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                    name="class_name",
                    description="Класс, которому будет выдано задание",
                    type=interactions.OptionType.STRING,
                    required=True,
                    autocomplete=True
                ),
                interactions.Option(
                    name="subject",
                    description="Предмет",
                    type=interactions.OptionType.STRING,
                    required=True,
                    choices=Subjects.subjects
                ),
                interactions.Option(
                    name="number",
                    description="Номер задания",
                    type=interactions.OptionType.INTEGER,
                    required=True
                )
            ]
        )
    ]
)
async def TaskCommand(ctx: interactions.CommandContext, sub_command: str, subject: str,
                      number: int = 0, class_name: str = ""):
    if sub_command == "find":
        await FindTask(subject, number, ctx)
    elif sub_command == "give":
         # TODO: Выдача задания классу
         raise NotImplementedError


async def SolveTaskButtonPress(ctx: interactions.ComponentContext, taskId: str):
    task: TaskModel = TaskCache[taskId]
    if task.solved:
        await ctx.send("Вы уже ответили на этот вопрос", ephemeral=True)
        return

    modal = interactions.Modal(
        title="Ответ на вопрос",
        custom_id=f"answerModar_{taskId}",
        components=[
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label="Введите ответ",
                custom_id="answerInputField",
                min_length=1,
                max_length=255
            )
        ]
    )
    await ctx.popup(modal)


async def ModalResponseHandler(ctx, taskId: str):
    task: TaskModel = TaskCache[taskId]
    if task.solved:
        await ctx.send("Вы уже ответили на этот вопрос", ephemeral=True)
        return
    answer = ctx._json['data']['components'][0]['components'][0]['value']

    if task.tryToSolve(answer):
        components = []
        for e in task.analogs[0:5]:
            components.append(interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label=f"Зад. {e}",
                custom_id=f"analogTask_{task.subject}_{e}"
            ))
        row = interactions.ActionRow(components=components)

        await ctx.send(f"Правильно! Ваш балл - `{task.result}`\nПохожие задания:", components=row)

        db = DbConnection.CreateSession()
        db.query(Task).filter(Task.Id == taskId).update({"Result": task.result})
        db.commit()

        #TODO: добавить кнопок с "похожими номерами"
    else:
        await ctx.send("Неверный ответ")


@bot.event
async def on_interaction_create(interaction):
    if interaction.type == interactions.InteractionType.MESSAGE_COMPONENT:
        interaction: interactions.ComponentContext

        if interaction.custom_id.startswith("SolveTask_"):
            taskId = interaction.custom_id.split("_")[1]
            await SolveTaskButtonPress(interaction, taskId)

        elif interaction.custom_id.startswith("analogTask_"):
            subj = interaction.custom_id.split("_")[1]
            number = interaction.custom_id.split("_")[2]
            await FindTask(subj, int(number), interaction)

    elif interaction.type == interactions.InteractionType.MODAL_SUBMIT:
        custom_id = interaction._json['data']['custom_id']
        if custom_id.startswith("answerModar_"):
            taskId = custom_id.split("_")[1]
            await ModalResponseHandler(interaction, taskId)


async def SearchClass(ctx, userInput: str = ""):
    #TODO: сделать поиск названия класса в БД

    db = DbConnection.CreateSession()
    classes = db.query(Class).limit(25).all()
    choices = []
    for cla in classes:
        cla: Class
        choices.append(interactions.Choice(name=cla.ClassName, value=str(cla.Id)))

    await ctx.populate(choices)


@bot.command(
    name="teacher",
    description="Управлять учителями",
    scope=GuildIDS,
    options=[
        interactions.Option(
            name="add",
            description="Добавить учителя",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                name="user",
                description="Пользователь, который будет учителем",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        ),
        interactions.Option(
            name="remove",
            description="Убрать учителя",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                name="user",
                description="Пользователь, который больше будет учителем",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        )
    ]
)
async def TeacherCommand(ctx: interactions.CommandContext, sub_command: str,
                         user: interactions.Member = None):
    if sub_command == "add":
        teacher: User = User()
        teacher.IsTeacher = True

        db_sess = DbConnection.CreateSession()
        db_sess.add(teacher)
        db_sess.commit()

    elif sub_command == "remove":
        # TODO: Убрать учителя

        raise NotImplementedError


@bot.command(
    name="class",
    description="Управлять классами",
    scope=GuildIDS,
    options=[
        interactions.Option(
            name="create",
            description="Добавить класс",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                name="class_name",
                description="Название класса",
                type=interactions.OptionType.STRING,
                required=True
                )
            ]
        ),
        interactions.Option(
            name="remove",
            description="Убрать класс",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                name="class_id",
                description="Название класса",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
                )
            ]
        ),
        interactions.Option(
            name="add_student",
            description="Добавить ученика в класс",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                name="class_id",
                description="Название класса",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
                ),
                interactions.Option(
                name="user",
                description="Ученик, который будет добавлен в класс",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        ),
        interactions.Option(
            name="remove_student",
            description="Убрать ученика из класса",
            type=interactions.OptionType.SUB_COMMAND,
            required=False,
            options=[
                interactions.Option(
                name="class_id",
                description="Название класса",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
                ),
                interactions.Option(
                name="user",
                description="Ученик, который будет убран из класса",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        )
    ]
)
async def ClassComand(ctx: interactions.CommandContext, sub_command: str,
                         user: interactions.Member = None, class_id: str = "", class_name: str = ""):
    await ctx.defer()
    class_id = int(class_id)

    if sub_command == "create":
        main_class = Class()
        main_class.ClassName = class_name

        db_sess = DbConnection.CreateSession()
        if db_sess.query(Class).filter(Class.ClassName == class_id).first() is not None:
            await ctx.send("Этот класс уже существует в системе")
            return

        db_sess.add(main_class)
        db_sess.commit()

        await ctx.send("Класс добавлен")

    elif sub_command == "remove":
        db_sess = DbConnection.CreateSession()
        if (cl := db_sess.query(Class).filter(Class.Id == class_id)).first() is None:
            await ctx.send("Класс не найден")
            return

        cl.delete()
        db_sess.commit()

        await ctx.send("Класс удалён")
    elif sub_command == "add_student":
        # TODO: Добавить ученика в класс

        raise NotImplementedError
    elif sub_command == "remove_student":
        # TODO: Убрать ученика из класс

        raise NotImplementedError


@bot.command(
    name="tasks",
    description="Вывод всех заданий",
    scope=GuildIDS
)
async def GetTasks(ctx: interactions.CommandContext):
    # TODO: вывод списка заданий для текущего ученика

    raise NotImplementedError


@bot.autocomplete(command="task", name="class_name")
async def SearchClassByNameAutocomplete(ctx, user_input: str = ""):
    await SearchClass(ctx, user_input)


@bot.autocomplete(command="class", name="class_id")
async def SearchClassByNameAutocomplete(ctx, user_input: str = ""):
    await SearchClass(ctx, user_input)


if __name__ == "__main__":
    log("Starting bot...", loglevel=LogLevel.INFO)
    bot.start()

