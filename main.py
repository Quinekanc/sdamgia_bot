from enums.LogLevel import LogLevel
from sdamgia import SdamGIA
import interactions
from interactions.api.models.misc import MISSING
from utils.Log import log, InitLogger
from models import DbConnection
import json


with open("token.txt", mode='r', encoding='utf8') as f:
    TOKEN = f.read()

with open("guildIDs.json", mode='r', encoding='utf8') as f:
    data = json.loads(f.read())
    if len(data['ids']) == 0:
        GuildIDS = MISSING
    else:
        GuildIDS = data['ids']


bot = interactions.Client(token=TOKEN, intents=interactions.Intents.ALL)

#sdamgia = SdamGIA()
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
                             description=f"""    
    `Ping={bot.latency}ms`
    """,
                             color=0xff00)

    await ctx.send(embeds=[emb])


if __name__ == "__main__":
    log("Starting bot...", loglevel=LogLevel.INFO)
    bot.start()

