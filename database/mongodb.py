from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI")
)

db = client["hr"]

users_collection = db["admin"]
jobs_collection = db["jobs"]
candidates_collection = db["candidates"]