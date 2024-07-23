from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('DB_URI'), server_api=ServerApi('1'))
db=client["event_management_system"]

try:
    client.admin.command('ping')
    # print("hello")
except Exception as e:
    print(e)