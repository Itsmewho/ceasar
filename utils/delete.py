from colorama import Fore, Style
from db.db_operations import read_db, update_db, delete_db
from utils.helpers import (
    typing_effect,
    pauze_clear,
)


def delete_user(user_phone):

    try:

        delete_db("users", {"phone": user_phone})
        typing_effect(
            Fore.GREEN
            + f"User {user_phone} deleted from the users collection."
            + Style.RESET_ALL
        )

        contact_lists = read_db("contact_list", {"contacts.phone": user_phone})
        for contact_list in contact_lists:

            update_db(
                "contact_list",
                {"_id": contact_list["_id"]},
                {"$pull": {"contacts": {"phone": user_phone}}},
            )
            typing_effect(
                Fore.GREEN
                + f"User {user_phone} removed from a contact list."
                + Style.RESET_ALL
            )

        delete_db(
            "messages",
            {"$or": [{"sender_phone": user_phone}, {"recipient_phone": user_phone}]},
        )
        typing_effect(
            Fore.GREEN
            + f"All messages sent or received by {user_phone} deleted."
            + Style.RESET_ALL
        )
        pauze_clear()

        typing_effect(
            Fore.GREEN
            + f"User {user_phone} account has been fully deleted!"
            + Style.RESET_ALL
        )

    except Exception as e:
        typing_effect(Fore.RED + f"Error deleting user: {e}" + Style.RESET_ALL)
