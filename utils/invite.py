from utils.helpers import *
from colorama import Fore, Style
from models.invites import InviteModel
from db.db_operations import create_db, read_db, update_db, delete_db


def send_invite(
    sender_name,
    sender_surname,
    sender_phone,
    recipient_name,
    recipient_surname,
    recipient_phone,
    message,
):
    sender_contact_list = read_db(
        {
            "user_name": sender_name,
            "user_surname": sender_surname,
            "user_phone": sender_phone,
        },
    )
    if sender_contact_list:
        contacts = sender_contact_list[0].get("contacts", [])
        for contact in contacts:
            if (
                contact["phone"] == recipient_phone
                and contact["name"] == recipient_name
                and contact["surname"] == recipient_surname
            ):
                return False, f"Invite already sent to {recipient_name}."

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

    existing_invite = read_db(
        "invitations",
        {
            "sender_name": sender_name,
            "sender_phone": sender_phone,
            "recipient_phone": recipient_phone,
            "status": "unread",
        },
    )
    if existing_invite:
        clear()
        return (
            False,
            Fore.RED
            + f"An invite is already pending for {recipient_name} {recipient_surname}. {Style.RESET_ALL}",
        )

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
        clear()
        return True, Fore.BLUE + f"Invite sent successfully!{Style.RESET_ALL}"

    except Exception as e:
        return False, Fore.RED + f"Error sending invite: {e}{Style.RESET_ALL}"


def respond_invite(invite_id, response):
    try:
        invite = read_db("invitations", {"_id": invite_id})
        if not invite:
            return False, "Invite not found."

        invite = invite[0]
        sender = {
            "name": invite["sender_name"],
            "surname": invite["sender_surname"],
            "phone": invite["sender_phone"],
        }

        recipient = {
            "name": invite["recipient_name"],
            "surname": invite["recipient_surname"],
            "phone": invite["recipient_phone"],
        }

        if response.lower() in ["accept", "a"]:
            add_contact(sender["name"], sender["surname"], sender["phone"], recipient)
            add_contact(
                recipient["name"], recipient["surname"], recipient["phone"], sender
            )

            update_db("invitations", {"_id": invite_id}, {"status": "accepted"})

            delete_db("invitations", {"_id": invite_id})

            return (
                True,
                Fore.BLUE + "Invite accepted and contacts updated." + Style.RESET_ALL,
            )

        elif response.lower() in ["decline", "d"]:

            update_db("invitations", {"_id": invite_id}, {"status": "declined"})
            delete_db("invitations", {"_id": invite_id})
            return True, "Invite declined and removed."

        else:
            return (
                False,
                Fore.RED
                + "Invalid response. Please enter 'accept' or 'decline'."
                + Style.RESET_ALL,
            )

    except Exception as e:
        return False, f"Error responding to invite: {e}"


def add_contact(user_name, user_surname, user_phone, contact):
    try:
        secure_id = generate_secure_id()

        contact_data = {
            "name": contact["name"],
            "surname": contact["surname"],
            "phone": contact["phone"],
            "secure_id": secure_id,
        }

        user_contact_list = read_db("contact_list", {"user_phone": user_phone})

        if not user_contact_list:
            typing_effect(
                Fore.GREEN
                + f"Creating new contact list for {user_name} {user_surname}...{Style.RESET_ALL}"
            )

            create_db(
                "contact_list",
                {
                    "user_name": user_name,
                    "user_surname": user_surname,
                    "user_phone": user_phone,
                    "contacts": [],
                },
            )
            user_contact_list = [
                {
                    "user_name": user_name,
                    "user_surname": user_surname,
                    "user_phone": user_phone,
                    "contacts": [],
                }
            ]
            pauze_clear()

        # Debug logs to check if contact is being added
        print(
            f"Adding contact {contact_data['name']} {contact_data['surname']} to {user_name}'s contact list."
        )

        update_db(
            "contact_list",
            {"user_phone": user_phone},
            {"$addToSet": {"contacts": contact_data}},
        )

        return True

    except Exception as e:
        return False, f"Error adding contact: {e}{Style.RESET_ALL}"


def manage_invites(user_phone):
    invites = read_db(
        "invitations", {"recipient_phone": user_phone, "status": "unread"}
    )

    if not invites:
        pauze_clear()
        typing_effect(Fore.BLUE + f"You have no unread invites.{Style.RESET_ALL}")
        return

    typing_effect(
        Fore.GREEN + f"You have {len(invites)} unread invite(s):{Style.RESET_ALL}"
    )
    for item, invite in enumerate(invites, 1):
        typing_effect(
            f"{item}. From {invite['sender_name']} {invite['sender_surname']} - Message: {invite['message']}"
        )

    while True:
        choice = input_typing_effect(
            "Enter the number of the invite, 'b' to go back, or 'q' to quit: "
        ).lower()
        clear()
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

            if next_action in ["back", "b"]:
                clear()
                return
            elif next_action in ["view", "v"]:
                clear()
                continue
            else:
                typing_effect(
                    Fore.RED
                    + f"Invalid option, going back to the main menu.{Style.RESET_ALL}"
                )
                pauze_clear()
                return
        else:
            typing_effect(
                Fore.RED
                + "Invalid choice. Please enter a valid option."
                + Style.RESET_ALL
            )
