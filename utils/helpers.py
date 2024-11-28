import os
import time
import random


def clear():
    time.sleep(0.35)
    os.system("cls" if os.name == "nt" else "clear")


def typing_effect(message, delay=0.035):

    for char in message:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def input_typing_effect(prompt, delay=0.035):
    for char in prompt:
        print(char, end="", flush=True)
        time.sleep(delay)
    user_input = input().strip().lower()

    if user_input == "quit":
        handle_quit()

    return user_input


def pauze_clear(delay=0.35, message=None, typing_delay=0.075):

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


def get_valid_response(prompt, valid_response, quit_response):
    # Will delete this one ?
    while True:
        response = input_typing_effect(prompt).lower()
        if response in valid_response:
            return response
        elif response in quit_response:
            return "quit"
        typing_effect("Invalid response. Please try again")
        pauze_clear(message=None)
