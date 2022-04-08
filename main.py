from enums.LogLevel import LogLevel
from sdamgia import SdamGIA
import interactions
from interactions.api.models.misc import MISSING
from utils.Log import log, InitLogger
from models import DbConnection
import json
from data import Subjects


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
DbConnection.InitDb("db.sqlite")


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

@bot.command(
    name="task",
    description="Получить задание",
    scope=GuildIDS,
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
)
async def TaskCommand(ctx: interactions.CommandContext, subject: str, number: int):
    try:
        result = sdamgia.get_problem_by_id(subject, str(number))
    except Exception as ex:
        log(ex, loglevel=LogLevel.ERROR)
        await ctx.send("Произошла ошибка")
        return

    if result is None:
        await ctx.send("Задание не найдено", ephemeral=True)
        return

    emb = interactions.Embed(title=f"Задание №{number}",
                             description=f"""`{result["condition"]["text"]}`""",
                             color=0xff00)

    await ctx.send(embeds=[emb])


if __name__ == "__main__":
    log("Starting bot...", loglevel=LogLevel.INFO)
    bot.start()

