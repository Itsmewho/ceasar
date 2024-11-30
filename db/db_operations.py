import os
from dotenv import load_dotenv
from pymongo import MongoClient
from colorama import Fore, Style


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

MONGO_DBNAME = os.getenv("MONGO_DBNAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]


def create_db(collection_name, data):

    try:
        db[collection_name].insert_one(data)
        # print(Fore.GREEN + f"Document inserted into {collection_name}{Style.RESET_ALL}") --> It works only for debugging
    except Exception as e:
        print(Fore.RED + f"Error inserting document: {e}{Style.RESET_ALL}")


def read_db(collection_name, query=None):

    try:
        if query is None:
            query = {}
        return list(db[collection_name].find(query))
    except Exception as e:
        print(Fore.RED + f"Error reading data : {e}{Style.RESET_ALL}")
        return []


def update_db(collection_name, query, update_data):
    try:

        if "$set" not in update_data:
            update_data = {"$set": update_data}

        result = db[collection_name].update_one(query, update_data)
        if result.modified_count > 0:
            print(
                Fore.GREEN
                + f"Document is updated in {collection_name}{Style.RESET_ALL}"
            )
        else:
            print(Fore.BLUE + f"No matched documents{Style.RESET_ALL}")
    except Exception as e:
        print(Fore.RED + f"Error updating data : {e}{Style.RESET_ALL}")


def delete_db(collection_name, query):

    try:
        result = db[collection_name].delete_one(query)
        if result.deleted_count > 0:
            print(Fore.GREEN + f"Deleted : {collection_name} {Style.RESET_ALL}")
        else:
            print(Fore.BLUE + f"No documents matched{Style.RESET_ALL}")
    except Exception as e:
        print(Fore.RED + f"Error deleting document: {e} {Style.RESET_ALL}")
