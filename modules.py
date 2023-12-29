import os
import subprocess
import sys
import time
import threading
args=sys.argv
args= [arg.lower() for arg in args]
def countdown_sleep(time:int,reason:str=None):
    for i in range(time):
        print(f"{reason if reason else 'continue'} in {time-i}")
        time.sleep(1)
class Fore:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
class Back:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
RESET = '\033[0m'
def info(message:str) -> None:
    print(f"{Fore.BLACK}{Back.BLUE}{message}{RESET}")
def warn(message:str) -> None:
    print(f"{Fore.BLACK}{Back.YELLOW}{message}{RESET}")
def error(message:str) -> None:
    return f"{Fore.BLACK}{Back.RED}{message}{RESET}"
def success(message:str) -> None:
    print(f"{Fore.BLACK}{Back.GREEN}{message}{RESET}")
def get_interfaces():
    wifi_interfaces = subprocess.check_output("iwconfig").decode().split("\n")
    for line in wifi_interfaces[:]:
        if not "wlan" in line:
            wifi_interfaces.remove(line)
    for i,interface in enumerate(wifi_interfaces[:]):
        rest = interface.split("  ")
        name = rest[0]
        mode = rest[3] if rest[3].startswith("Mode") else "Mode:Managed"
        wifi_interfaces[i] = [name,mode]
    return wifi_interfaces
def inlineraise(message):
    raise Exception(error(message))
ir=inlineraise