import os
import re
import time
import bcrypt
import msvcrt
import getpass
from colorama import Fore, Style
from db.db_operations import read_db
from pydantic import BaseModel, ValidationError

# General use:


def clear():
    time.sleep(0.35)
    os.system("cls" if os.name == "nt" else "clear")


def typing_effect(message, delay=0.02):
    for char in message:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def input_typing_effect(prompt, delay=0.02):
    for char in prompt:
        print(char, end="", flush=True)
        time.sleep(delay)
    user_input = input().strip().lower()

    if user_input in ["n", "q", "quit"]:
        handle_quit()
    return user_input


def input_with_masking(prompt, delay=0.02):

    try:
        delay = float(delay)
    except ValueError:
        delay = 0.02

    for char in prompt:
        print(char, end="", flush=True)
        time.sleep(delay)

    if os.name == "nt":  # Windows
        user_input = ""
        while True:
            char = msvcrt.getch()  # Get a single character from the user
            if char == b"\r":  # Enter key pressed
                break
            elif char == b"\x08":  # Backspace key pressed
                user_input = user_input[:-1]
                print("\b \b", end="", flush=True)  # Remove the last character
            else:
                user_input += char.decode("utf-8")
                print("*", end="", flush=True)  # Print * to mask input
        print()  # Newline after input

    else:  # Linux/macOS (Unix-based systems)
        user_input = getpass.getpass(
            prompt
        )  # Use getpass for Unix-based systems (masks input)
        print()  # Newline after input

    return user_input


def pauze_clear(delay=0.35, message=None):
    time.sleep(delay)
    clear()
    if message:
        for char in message:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()


def handle_quit():
    typing_effect(Fore.BLUE + f"Goodbye, Till next time! {Style.RESET_ALL}")
    pauze_clear(message=None)
    exit()


# Encrypt and Decryption functions:


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return bcrypt.hashpw(password.encode("utf-8"), salt)


def check_password(stored_password, entered_password):
    return bcrypt.checkpw(
        entered_password.encode("utf-8"), stored_password.encode("utf-8")
    )


# Register functions:


def check_user_exists(name, surname, phone, email):

    email = email.lower()
    phone = phone.strip()

    existing_user = read_db(
        "users", {"name": name, "surname": surname, "phone": phone, "email": email}
    )
    return len(existing_user) > 0


def validate_field(field_name, value):

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if field_name == "email":
        # Manually validate the email using regex
        if not re.match(email_regex, value):
            return "Invalid email format"

    class TempModel(BaseModel):
        __annotations__ = {field_name: str}

    try:
        TempModel(**{field_name: value})  # Validate the field
        return True

    except ValidationError as e:
        return e.errors()[0]["msg"]


def get_valid_input_validation(prompt, field_type, min_length=None):

    while True:
        user_input = input_typing_effect(prompt).title()

        # If we have a min_length requirement (e.g., for password or phone), validate it
        if min_length and len(user_input) < min_length:
            typing_effect(
                Fore.RED
                + f"{field_type.capitalize()} must be at least {min_length} characters long. Please try again."
                + Style.RESET_ALL
            )
            continue

        validation = validate_field(field_type, user_input)
        if validation is True:
            return user_input
        typing_effect(Fore.RED + f"Invalid {field_type}: {validation}{Style.RESET_ALL}")


# Login functions:


def check_user_login(name, surname, phone, password):

    try:
        # Query the database for the user
        user = read_db("users", {"name": name, "surname": surname, "phone": phone})

        if user:
            user = user[0]
            stored_password = user["password"]

            # Validate password
            if check_password(stored_password, password):
                return True, user
            return False, "Incorrect password."
        return False, "User not found."

    except Exception as e:
        return False, f"Error checking user: {e}"
