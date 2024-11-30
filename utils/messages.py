from datetime import datetime
from colorama import Fore, Style
from db.db_operations import create_db, read_db, update_db
from utils.helpers import (
    caesar_encrypt,
    caesar_decrypt,
    typing_effect,
)


def send_message(sender, recipient_phone, message):

    try:
        sender_contacts = read_db("contact_list", {"user_phone": sender["phone"]})

        if not sender_contacts or not sender_contacts[0].get("contacts"):
            return False, Fore.RED + f"Recipient not found in your contact list."

        contact = next(
            (
                c
                for c in sender_contacts[0]["contacts"]
                if c["phone"] == recipient_phone
            ),
            None,
        )
        if not contact:
            return False, Fore.RED + f"Recipient not found in your contact list."

        shift = 3
        print(f"Original message: {message}")
        print(f"Shift value: {shift}")

        encrypted_message = caesar_encrypt(message, shift)

        print(f"Encrypted message: {encrypted_message}")

        message_data = {
            "sender_name": sender["name"],
            "sender_phone": sender["phone"],
            "recipient_name": contact["name"],
            "recipient_phone": recipient_phone,
            "encrypted_message": encrypted_message,
            "timestamp": datetime.now(),
            "status": "unread",
        }

        create_db("messages", message_data)
        return (
            True,
            Fore.GREEN
            + f"Message sent successfully to {contact['name']}.{Style.RESET_ALL}",
        )

    except Exception as e:
        return False, Fore.RED + f"Error sending message: {e}{Style.RESET_ALL}"


def read_messages(user_phone):
    try:
        messages = read_db(
            "messages", {"recipient_phone": user_phone, "status": "unread"}
        )

        if not messages:
            typing_effect("No unread messages.")
            return [], "No unread messages."

        for msg in messages:
            print("\n----------------------------------------")
            print(f"From: {msg['sender_name']} ({msg['sender_phone']})")
            print(f"Message: {msg['encrypted_message']}")

            # Retrieve sender contact from the user's contact list
            sender_contact = next(
                (
                    contact
                    for contact in read_db("contact_list", {"user_phone": user_phone})[
                        0
                    ]["contacts"]
                    if contact["phone"] == msg["sender_phone"]
                ),
                None,
            )

            if not sender_contact:
                print("Could not decrypt the message. Sender not in your contact list.")
            else:
                shift = 3
                decrypted_message = caesar_decrypt(msg["encrypted_message"], shift)
                print(f"Decrypted Message: {decrypted_message}")

            print(f"Received: {msg['timestamp']}")
            print("----------------------------------------")

            update_db("messages", {"_id": msg["_id"]}, {"status": "read"})

        return messages, "Unread messages retrieved successfully."

    except Exception as e:
        typing_effect(f"Error reading messages: {e}")
        return None, f"Error reading messages: {e}"
