from utils.helpers import *
from colorama import Fore, Style
from utils.register import register, login


def main():
    typing_effect(Fore.GREEN + f"Welcome to Caesar Cipher Messages!")

    while True:
        register()
        input_typing_effect("Do you want to register another user? (y/n): ").lower()


if __name__ == "__main__":
    main()
