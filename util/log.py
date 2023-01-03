from colorama import Fore
from datetime import datetime

def init():
    open("log.txt","w", encoding="utf-8").close()

init()

def append_log(msg: str):
    fd = open("log.txt", mode="a+", encoding="utf-8")
    fd.write(msg + "\n")
    fd.close()

def log_green(msg: str):
    print(Fore.GREEN + "[SUCCESS] " + Fore.WHITE + msg)
    append_log(msg=f"[{datetime.now().utcnow()}] {msg}")
def log_red(msg: str):
    print(Fore.RED + "[ERROR] " + Fore.WHITE + msg)
    append_log(msg=f"[{datetime.now().utcnow()}] {msg}")