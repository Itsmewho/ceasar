from utils.helpers import *
from colorama import Fore, Style
from models.users import UserModel
from db.db_operations import create_db


def main():

    typing_effect(Fore.GREEN + f"Welcome to Ceasar Cipher Messages!")

    name = get_valid_input("Enter your first name: ", "name").title()
    surname = get_valid_input("Enter your surname: ", "surname").title()
    email = get_valid_input("Enter your email: ", "email").lower()
    phone = get_valid_input("Enter your phone number: ", "phone")

    if check_user_exists(name, surname, phone):
        typing_effect(Fore.RED + "User already exists!" + Style.RESET_ALL)
        if input_typing_effect("Do you want to retry? (y/n): ").lower() != "y":
            handle_quit()
            return

    # Password validation :

    while True:
        password = get_valid_input(
            "Enter your password (min length is 8): ", "password"
        )
        confirm_pass = input_typing_effect("Confirm password: ")
        if password != confirm_pass:
            typing_effect(
                Fore.RED
                + f"Passwords do not match! Please try again. {Style.RESET_ALL}"
            )
        else:
            break

    try:
        user_data = UserModel(
            name=name, surname=surname, email=email, phone=phone, password=password
        )

        encrypted_password = encrypt_password(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["password"] = encrypted_password.decode("utf-8")
        create_db("users", user_data_dict)
        typing_effect("User registered successfully!")

    except ValueError as e:
        typing_effect(f"Error: {e}")


if __name__ == "__main__":
    while True:
        main()
        input_typing_effect("Do you want to register another user? (y/n): ").lower()
