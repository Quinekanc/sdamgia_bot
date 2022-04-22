import os

from DBmodels.ClassTask import ClassTask
from DBmodels.ClassTeacher import ClassTeacher
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
from enums import Subject
from DBmodels.Class import Class
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


bot = interactions.Client(token=TOKEN, intents=interactions.Intents.ALL, disable_sync=False)

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


def AddUserToDb(user):
    db = DbConnection.CreateSession()
    if db.query(User).filter(User.Id == int(user.id)).first() is None:
        usr = User()
        usr.Id = int(user.id)
        db.add(usr)
        db.commit()


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
                    name="class_id",
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
                      number: int = 0, class_id: str = ""):
    AddUserToDb(ctx.author)
    await ctx.defer()

    if sub_command == "find":
        await FindTask(subject, number, ctx)
    elif sub_command == "give":
        db = DbConnection.CreateSession()

        if not db.query(User).filter(User.Id == int(ctx.author.id)).first().IsTeacher:
            await ctx.send("Вы не учитель!")
            return

        task = ClassTask()
        task.TaskId = number
        task.SubjectId = subject
        task.TeacherId = int(ctx.author.id)
        task.ClassId = class_id

        db.add(task)
        db.commit()

        await ctx.send("Задание выдано классу")


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
    db = DbConnection.CreateSession()
    classes = db.query(Class).filter(Class.ClassName.ilike(f"%{userInput}%")).limit(25).all()
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
    AddUserToDb(ctx.author)
    AddUserToDb(user)

    if sub_command == "add":
        db_sess = DbConnection.CreateSession()
        db_sess.query(User).filter(User.Id == int(user.id)).update({"IsTeacher": True})
        db_sess.commit()

        await ctx.send("Учитель добавлен")

    elif sub_command == "remove":
        db_sess = DbConnection.CreateSession()
        db_sess.query(User).filter(User.Id == int(user.id)).update({"IsTeacher": False})
        db_sess.commit()

        await ctx.send("Учитель удалён")


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
                name="user",
                description="Ученик, который будет убран из класса",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        ),
        interactions.Option(
            name="add_teacher",
            description="Добавить учителя в класс",
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
                description="Учитель, который будет добавлен в класс",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        ),
        interactions.Option(
            name="remove_teacher",
            description="Убрать учителя из класса",
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
                description="Учитель, который будет убран из класса",
                type=interactions.OptionType.USER,
                required=True
                )
            ]
        )
    ]
)
async def ClassComand(ctx: interactions.CommandContext, sub_command: str,
                      user: interactions.Member = None, class_id: str = None,
                      class_name: str = None):
    await ctx.defer()

    AddUserToDb(ctx.author)

    if user is not None:
        AddUserToDb(user)

    if class_id is not None:
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
        db = DbConnection.CreateSession()
        q = db.query(User).filter(User.Id == int(user.id))
        if q.first().ClassId is not None:
            await ctx.send("Пользователь уже состоит в классе")
            return

        q.update({"ClassId": class_id})
        db.commit()
        await ctx.send("Участник добавлен в класс")

    elif sub_command == "remove_student":

        db = DbConnection.CreateSession()
        q = db.query(User).filter(User.Id == int(user.id))
        if q.first().ClassId is None:
            await ctx.send("Пользователь и так не состоял ни в одном классе")
            return

        q.update({"ClassId": None})
        db.commit()
        await ctx.send("Участник удалён из класса")

    elif sub_command == "add_teacher":
        db = DbConnection.CreateSession()

        usr: User = db.query(User).filter(User.Id == int(user.id)).first()

        if usr is None:
            await ctx.send("Участник не учитель")
            return

        if class_id in [e.Id for e in usr.classes]:
            await ctx.send("Участник уже учитель в этом классе")
            return

        teacher = ClassTeacher()
        teacher.TeacherId = int(user.id)
        teacher.ClassId = class_id

        db.add(teacher)
        db.commit()

        await ctx.send("Учитель добавлен в класс")

    elif sub_command == "remove_teacher":
        db = DbConnection.CreateSession()

        usr: User = db.query(User).filter(User.Id == int(user.id)).first()

        if class_id not in [e.Id for e in usr.classes]:
            await ctx.send("Участник и так не учитель в этом классе")
            return

        db.query(ClassTeacher).filter(ClassTeacher.ClassId == class_id
                                      and ClassTeacher.TeacherId == int(user.id)).delete()
        db.commit()

        await ctx.send("Учитель удалён из класса")


@bot.command(
    name="tasks",
    description="Вывод заданий",
    scope=GuildIDS
)
async def GetTasks(ctx: interactions.CommandContext):
    await ctx.defer()

    AddUserToDb(ctx.author)

    db = DbConnection.CreateSession()

    user: User = db.query(User).filter(User.Id == int(ctx.author.id)).first()
    if user.ClassId is None:
        await ctx.send("Вы не состоите ни в одном в классе")
        return

    cla: Class = db.query(Class).filter(Class.Id == user.ClassId).first()
    if len(cla.Tasks) == 0:
        text = "Заданий нет"
    else:
        data = []
        for task in cla.Tasks:
            data.append("`Предмет:     Номер:`")
            data.append(f"`{getattr(Subject.Subjects, task.SubjectId)} - {task.TaskId}`")

        text = "\n".join(data)
    await ctx.send(text)


@bot.command(
    name="solved-tasks",
    description="Вывод решённых заданий",
    scope=GuildIDS
)
async def GetSolvedTasks(ctx: interactions.CommandContext):
    await ctx.defer()
    AddUserToDb(ctx.author)

    db = DbConnection.CreateSession()
    desc = []
    desc.append("`Предмет:     Балл:`")
    for task in db.query(Task).filter(Task.StudentId == int(ctx.author.id)).limit(50).all():
        if task.Result is not None:
            desc.append(f"`{getattr(Subject.Subjects, task.SubjectId)} - {task.Result}`")

    emb = interactions.Embed(title="Решённые задания", color=0xff00, description="\n".join(desc))
    await ctx.send(embeds=[emb])


@bot.autocomplete(command="task", name="class_id")
async def SearchClassByNameAutocomplete(ctx, user_input: str = ""):
    await SearchClass(ctx, user_input)


@bot.autocomplete(command="class", name="class_id")
async def SearchClassByNameAutocomplete(ctx, user_input: str = ""):
    await SearchClass(ctx, user_input)


if __name__ == "__main__":
    log("Starting bot...", loglevel=LogLevel.INFO)
    bot.start()

