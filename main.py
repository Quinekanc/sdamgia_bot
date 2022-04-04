from enums.LogLevel import LogLevel
from sdamgia import SdamGIA
import interactions
from interactions.api.models.misc import MISSING
from utils.Log import log
import json


with open("token.txt", mode='r', encoding='utf8') as f:
    TOKEN = f.read()

with open("guildIDs.json", mode='r', encoding='utf8') as f:
    data = json.loads(f.read())
    if len(data['ids']) == 0:
        GuildIDS = MISSING
    else:
        GuildIDS = data['ids']


bot = interactions.Client(token=TOKEN)

sdamgia = SdamGIA()

@bot.event
async def on_ready():
    log(f"Logged into {bot.me.name}", loglevel=LogLevel.INFO)


if __name__ == "__main__":
    bot.start()


@bot.command(
    name="status",
    description="Get bot's status",
    scope=
)
