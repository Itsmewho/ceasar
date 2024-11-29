import os
import time
import bcrypt
from colorama import Fore, Style
from models.users import UserModel
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

    if user_input == ["n", "q", "quit"]:
        handle_quit()
    return user_input


def get_valid_input(prompt, field_name):
    while True:
        user_input = input_typing_effect(prompt)
        validation = validate_field(field_name, user_input)
        if validation is True:
            return user_input
        # Can't find a better way for this,.. :
        typing_effect(Fore.RED + f"Invalid {field_name}: {validation}{Style.RESET_ALL}")


def pauze_clear(delay=0.35, message=None):
    time.sleep(delay)
    clear()
    if message:
        for char in message:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()


def handle_quit():
    typing_effect("Goodbye, Till next time!")
    pauze_clear(message=None)
    exit()


# Encrypt and Decription functions:


def encrypt_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


# Register functions:


def check_user_exists(name, surname, phone):
    existing_user = read_db("users", {"name": name, "surname": surname, "phone": phone})
    return len(existing_user) > 0


def validate_field(field_name, value):
    # pydantic model:
    class TempModel(BaseModel):
        __annotations__ = {field_name: str}

    try:
        TempModel(**{field_name: value})  # Validate the field
        return True

    except ValidationError as e:
        return e.errors()[0]["msg"]


# Login functions:
