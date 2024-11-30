from colorama import Fore, Style

from utils.helpers import *
from utils.auth import register, login
from utils.invite import manage_invites
from utils.login_menu import menu_after_login


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
            clear()
            register()
            continue

        elif action in ["login", "log", "l"]:
            logged_user = login()
            if logged_user:
                clear()
                typing_effect(
                    Fore.BLUE + f"Welcome back, {logged_user["name"]}{Style.RESET_ALL}"
                )
                pauze_clear()
                menu_after_login(logged_user)

        elif action in ["n", "q", "quit"]:
            handle_quit()  # Gracefully exit the program
            break  # Exit out of the main loop
        else:
            typing_effect(
                Fore.RED + "Invalid choice, please type 'login' or 'register'."
            )
            continue


if __name__ == "__main__":
    main()
