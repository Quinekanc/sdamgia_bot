from enums.LogLevel import LogLevel
from sdamgia import SdamGIA
import interactions
from utils.Log import log

TOKEN = ""


with open("token.txt", mode='r', encoding='utf8') as f:
    TOKEN = f.read()

bot = interactions.Client(token=TOKEN)

sdamgia = SdamGIA()

@bot.event
async def on_ready():
    log(f"Logged into {bot.me.name}", loglevel=LogLevel.INFO)


if __name__ == "__main__":
    bot.start()

