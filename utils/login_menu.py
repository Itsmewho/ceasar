from colorama import Style, Fore
from utils.invite_sys import manage_invites, send_invite
from utils.helpers import (
    input_typing_effect,
    typing_effect,
    handle_quit,
    clear,
    pauze_clear,
)


def menu_after_login(logged_user):
    logged_user_phone = logged_user[
        "phone"
    ]  # Use phone as the identifier for this session

    while True:
        action = input_typing_effect(
            "What do you want to do?\n1: manage invites\n2: send invite\n3: logout\n4: exit\nEnter choice: ",
        ).lower()

        if action == "1":
            # Manage unread invites
            manage_invites(logged_user_phone)

        elif action == "2":
            # Send a new invite
            recipient_phone = input_typing_effect("Enter recipient's phone number: ")
            recipient_name = input_typing_effect("Enter recipient's name: ").title()
            recipient_surname = input_typing_effect(
                "Enter recipient's surname: "
            ).title()
            message = input_typing_effect("Enter the invite message: ")

            result, message = send_invite(
                logged_user["name"],
                logged_user["surname"],
                logged_user_phone,
                recipient_name,
                recipient_surname,
                recipient_phone,
                message,
            )
            typing_effect(message)

        elif action == "3":
            # Log out
            typing_effect(Fore.GREEN + "Logging out...")
            return  # Go back to login

        elif action == "4":
            # Exit program
            handle_quit()

        else:
            typing_effect(
                Fore.RED + f"Invalid option, please choose again.{Style.RESET_ALL}"
            )
            pauze_clear()
