from utils.helpers import *
from colorama import Fore, Style
from models.users import UserModel
from db.db_operations import create_db


def register():

    while True:
        # Validate name, surname, email, and phone
        name = get_valid_input_validation(
            Fore.GREEN + f"Enter your first name: ", "name"
        ).title()
        surname = get_valid_input_validation(
            Fore.GREEN + f"Enter your surname: ", "surname"
        ).title()
        email = get_valid_input_validation(
            Fore.GREEN + f"Enter your email: ", "email"
        ).lower()

        validation = validate_field("email", email)
        if validation is not True:
            typing_effect(Fore.RED + f"Invalid email: {validation}{Style.RESET_ALL}")
            continue

        phone = get_valid_input_validation(
            Fore.GREEN + f"Enter your phone number: ", "phone", min_length=10
        )
        if not phone.isdigit():
            typing_effect(
                Fore.RED
                + "Invalid phone number. Please enter a valid phone number."
                + Style.RESET_ALL
            )
            continue

        # Check if the user already exists in the database
        if check_user_exists(name, surname, phone, email):
            typing_effect(
                Fore.RED
                + f"A user with the name '{name} {surname}' email: {email} and phone number '{phone}' already exists!"
                + Style.RESET_ALL
            )
            response = input_typing_effect("Do you want to retry? (y/n): ").lower()
            if response == "y":
                continue
            elif response in ["n", "q", "quit"]:
                handle_quit()
                break
            else:
                typing_effect(
                    Fore.RED + "Invalid response. Please enter 'y', 'n', or 'q'."
                )
                clear()
        else:
            break

    # Password validation
    while True:
        password = input_with_masking(
            Fore.GREEN + f"Enter your password (min length is 8): ", "password"
        )
        if len(password) < 8:
            typing_effect(
                Fore.RED
                + "Password must be at least 8 characters long. Please try again."
                + Style.RESET_ALL
            )
            continue
        confirm_pass = input_with_masking("Confirm password: ")
        if password != confirm_pass:
            typing_effect(
                Fore.RED
                + f"Passwords do not match! Please try again. {Style.RESET_ALL}"
            )
        else:
            break

    try:
        # User registration in Pydantic model
        user_data = UserModel(
            name=name, surname=surname, email=email, phone=phone, password=password
        )

        # Encrypt password before storing
        encrypted_password = encrypt_password(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["password"] = encrypted_password.decode("utf-8")

        # Save user data to the database
        create_db("users", user_data_dict)
        typing_effect(Fore.BLUE + f"User registered successfully! 👌 {Style.RESET_ALL}")

    except ValueError as e:
        typing_effect(f"Error: {e}")


def main():
    typing_effect(Fore.GREEN + f"Welcome to Caesar Cipher Messages!")

    while True:
        register()
        input_typing_effect("Do you want to register another user? (y/n): ").lower()


if __name__ == "__main__":
    main()
