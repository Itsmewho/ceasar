from utils.helpers import *
from models.invites import InviteModel
from colorama import Fore, Style


def send_invite(
    sender_name,
    sender_surname,
    sender_phone,
    recipient_name,
    recipient_surname,
    recipient_phone,
    message,
):

    sender = read_db(
        "users", {"name": sender_name, "surname": sender_surname, "phone": sender_phone}
    )
    recipient = read_db(
        "users",
        {
            "name": recipient_name,
            "surname": recipient_surname,
            "phone": recipient_phone,
        },
    )

    if not sender or not recipient:
        return False, Fore.RED + f"Either sender or recipient not found."
        pauze_clear()

    try:
        invite_data = InviteModel(
            sender_name=sender[0]["name"],
            sender_surname=sender[0]["surname"],
            sender_phone=sender_phone,
            recipient_name=recipient[0]["name"],
            recipient_surname=recipient[0]["surname"],
            recipient_phone=recipient_phone,
            message=message,
            status="unread",
        )
        invite_data_dict = invite_data.model_dump()

        create_db("invitations", invite_data_dict)
        return True, "Invite sent successfully!"
    except Exception as e:
        return False, f"Error sending invite: {e}"


def respond_invite(invite_id, response):

    if response.lower() in ["accept", "a"]:
        invite = read_db("invitations", {"_id": invite_id})[0]
        sender = invite["sender"]
        recipient = invite["recipient"]

        add_contact(sender["phone"], recipient)
        add_contact(recipient["phone"], sender)

        # Update the invite status to "accepted"
        update_db("invitations", {"_id": invite_id}, {"status": "accepted"})
        return True, "Invite accepted! Contacts updated."
    elif response.lower() in ["decline", "d"]:
        # Update the invite status to "declined"
        update_db("invitations", {"_id": invite_id}, {"status": "declined"})
        return True, "Invite declined."
    else:
        return False, "Invalid response."


def manage_invites(user_phone):
    # Fetch unread invites for the user based on their phone number
    invites = read_db(
        "invitations", {"recipient_phone": user_phone, "status": "unread"}
    )

    if not invites:
        pauze_clear()
        typing_effect(Fore.BLUE + f"You have no unread invites.{Style.RESET_ALL}")
        return

    # Display unread invites
    typing_effect(
        Fore.GREEN + f"You have {len(invites)} unread invite(s):{Style.RESET_ALL}"
    )
    for item, invite in enumerate(invites, 1):
        typing_effect(
            f"{item}. From {invite['sender_name']} {invite['sender_surname']} - Message: {invite['message']}"
        )

    while True:
        choice = input_typing_effect(
            "Enter the number of the invite you want to read, 'b' to go back, or 'q' to quit: "
        ).lower()

        if choice == "b":
            return
        elif choice == "q":
            handle_quit()
        elif choice.isdigit() and 1 <= int(choice) <= len(invites):
            invite = invites[int(choice) - 1]
            invite_id = invite["_id"]
            action_response = input_typing_effect(
                "Do you want to accept or decline? (accept/decline): "
            ).lower()

            if action_response in ["accept", "a"]:
                _, message = respond_invite(invite_id, "accept")
                typing_effect(message)
            elif action_response in ["decline", "d"]:
                _, message = respond_invite(invite_id, "decline")
                typing_effect(message)
            else:
                typing_effect("Invalid response. Please enter 'accept' or 'decline'.")

            next_action = input_typing_effect(
                "Do you want to view another invite or go back? (view/back): "
            ).lower()

            if next_action == "back":
                return
            elif next_action == "view":
                continue
            else:
                typing_effect("Invalid option, going back to the main menu.")
                return
        else:
            typing_effect(
                Fore.RED
                + "Invalid choice. Please enter a valid option."
                + Style.RESET_ALL
            )
