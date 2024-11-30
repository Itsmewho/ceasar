from colorama import Style, Fore
from utils.delete import delete_user
from utils.messages import send_message, read_messages
from utils.invite import manage_invites, send_invite
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
            Style.RESET_ALL + f"What do you want to do? \n"
            "(1) Manage invites\n"
            "(2) Send invites\n"
            "(3) Send message\n"
            "(4) Read messages\n"
            "(5) Delete account\n"
            "(6) Logout\n"
            "(7) Exit program\n"
            "Enter your choice: "
        ).strip()

        if action == "1":
            # Manage unread invites
            clear()
            manage_invites(logged_user_phone)

        elif action == "2":
            # Send a new invite
            pauze_clear()
            recipient_phone = input_typing_effect("Enter recipient's phone number: ")
            recipient_name = input_typing_effect("Enter recipient's name: ").title()
            recipient_surname = input_typing_effect(
                "Enter recipient's surname: "
            ).title()
            message = input_typing_effect("Enter the invite message: ")

            _, message = send_invite(
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
            # Send a message
            pauze_clear()
            recipient_phone = input_typing_effect(
                "Enter the recipient's phone number: "
            )
            message = input_typing_effect("Enter your message: ")
            result, feedback = send_message(logged_user, recipient_phone, message)
            typing_effect(feedback)

        elif action == "4":
            clear()
            messages, feedback = read_messages(logged_user["phone"])
            if messages:
                for msg in messages:
                    print(
                        f"From: {msg['sender_name']} - Message: {msg['encrypted_message']}"
                    )
            else:
                print(feedback)

        elif action == "5":
            # Delete the account
            confirm_delete = (
                input_typing_effect(
                    "Are you sure you want to delete your account? (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm_delete == "y":
                delete_user(logged_user_phone)
                break  # Exit the menu after account deletion
            else:
                typing_effect("Account deletion cancelled.")
                continue

        elif action == "6":
            typing_effect(Fore.GREEN + "Logging out...")
            break  # Go back to login

        elif action == "7":
            handle_quit()

        else:
            typing_effect(
                Fore.RED + f"Invalid option, please choose again.{Style.RESET_ALL}"
            )
            pauze_clear()
