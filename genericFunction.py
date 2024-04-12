import os
from colorama import init, Fore, Style

def limpaCmd():
    return os.system('cls')

def msgSucesso(msg):
    return print(Fore.GREEN + msg + Style.RESET_ALL)   

def msgErro(msg):
    return print(Fore.RED + msg + Style.RESET_ALL)   
