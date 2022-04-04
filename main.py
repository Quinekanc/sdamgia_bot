import datetime
from enums.LogLevel import LogLevel
from sdamgia import SdamGIA
import interactions
from colorama import init as ColoramaInit
from colorama import Fore, Back

ColoramaInit()


TOKEN = ""

def log(*args, loglevel=LogLevel.INFO):
    if loglevel == LogLevel.WARNING:
        prefix = f"{Fore.LIGHTYELLOW_EX}WARN{Fore.RESET}"
    elif loglevel == LogLevel.ERROR:
        prefix = f"{Fore.LIGHTRED_EX}ERR{Fore.RESET}"
    elif loglevel == LogLevel.CRITICAL:
        prefix = f"{Fore.BLACK}{Back.RED}CRIT{Fore.RESET}{Back.RESET}"
    else:
        prefix = f"{Fore.LIGHTGREEN_EX}INF{Fore.RESET}"

    print(f"[{datetime.datetime.now().strftime('%Y.%m.%d, %H:%M:%S')}][{prefix}] {' '.join([str(e) for e in args])}")


with open("token.txt", mode='r', encoding='utf8') as f:
    token = f.read()

bot = interactions.Client(token=TOKEN)

sdamgia = SdamGIA()

@bot.event
async def on_ready():
    log(f"Logged into {bot.me.name}", loglevel=LogLevel.INFO)



if __name__ == "__main__":
    bot.start()

