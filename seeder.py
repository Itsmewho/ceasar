import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from colorama import Style, Fore
from db.db_operations import create_db

# Load .env variables
load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DBNAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Testing databse

try:
    print(Fore.GREEN + f"Connected to MongoDB at {MONGO_URI}{Style.RESET_ALL}")
    print(f"Using database: {DB_NAME}")

    collections = db.list_collection_names()
    print("Collections:", collections)

except Exception as e:
    print(Fore.RED + f"Error connecting to MongoDB: {e}{Style.RESET_ALL}")

# load JSON's


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Seeding:


def seed_data():

    user_data = load_json("data/users.json")

    try:
        db["users"].drop()
        create_db("users", user_data[0])
        print(Fore.GREEN + f"User seeded suc6 {Style.RESET_ALL}")
    except Exception as e:
        print(Fore.RED + f"Error seeding users: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    seed_data()
