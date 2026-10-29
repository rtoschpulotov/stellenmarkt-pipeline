import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["jobsearch"]
collection = db["offene_stellen"]

ergebnis = collection.delete_many({})
print("Gelöschte Dokumente:", ergebnis.deleted_count)