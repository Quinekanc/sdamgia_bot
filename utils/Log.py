from enums.LogLevel import LogLevel
from colorama import Fore, Back
from colorama import init as ColoramaInit
import datetime


ColoramaInit()


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