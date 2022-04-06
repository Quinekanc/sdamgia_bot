from enums.LogLevel import LogLevel
from colorama import Fore, Back
from colorama import init as ColoramaInit
import datetime


ColoramaInit()

minimalLogLevel = LogLevel.INFO


def InitLogger(loglevel:int):
    global minimalLogLevel

    minimalLogLevel = loglevel


def log(*args, loglevel=LogLevel.INFO):
    prefix = None
    if loglevel == LogLevel.DEBUG and minimalLogLevel <= loglevel:
        prefix = f"DEBUG"
    elif loglevel == LogLevel.WARNING and minimalLogLevel <= loglevel:
        prefix = f"{Fore.LIGHTYELLOW_EX}WARN{Fore.RESET}"
    elif loglevel == LogLevel.ERROR and minimalLogLevel <= loglevel:
        prefix = f"{Fore.LIGHTRED_EX}ERR{Fore.RESET}"
    elif loglevel == LogLevel.CRITICAL and minimalLogLevel <= loglevel:
        prefix = f"{Fore.BLACK}{Back.RED}CRIT{Fore.RESET}{Back.RESET}"
    elif minimalLogLevel <= loglevel:
        prefix = f"{Fore.LIGHTGREEN_EX}INF{Fore.RESET}"

    if prefix is None:
        return
    print(f"[{datetime.datetime.now().strftime('%Y.%m.%d, %H:%M:%S')}][{prefix}] {' '.join([str(e) for e in args])}")