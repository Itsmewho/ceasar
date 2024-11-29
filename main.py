from utils.helpers import *
from colorama import Fore, Style
from utils.auth import register, login


def main():
    typing_effect(Fore.GREEN + f"Welcome to Caesar Cipher Messages!{Style.RESET_ALL}")
    typing_effect(
        Fore.BLUE + "Type 'quit' to exit the program at any time." + Style.RESET_ALL
    )

    while True:
        clear()
        action = input_typing_effect(
            "Do you want to login or register? (login/register): "
        ).lower()
        clear()
        if action in ["register", "r", "reg"]:
            # Clarification Run register:
            register()

        elif action in ["login", "log", "l"]:
            logged_user = login()
            if logged_user:
                typing_effect(Fore.GREEN + f"Welcome back, {logged_user["name"]}")
        else:
            typing_effect(
                Fore.RED
                + "Invalid choice. Please choose 'login' or 'register'."
                + Style.RESET_ALL
            )


if __name__ == "__main__":
    main()
