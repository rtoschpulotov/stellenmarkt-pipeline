import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
print("URI geladen")
client = MongoClient(mongo_uri)

client.admin.command("ping")
print("Verbindung erfolgreich")

db = client["jobsearch"]
collection = db["offene_stellen"]

test_dokument = {"titel": "Testeintrag", "quelle": "Verbindungstest"}
ergebnis = collection.insert_one(test_dokument)
print("Eingefügt mit ID:", ergebnis.inserted_id)

gefundenes_dokument = collection.find_one({"titel": "Testeintrag"})
print(gefundenes_dokument)

loesch_ergebnis = collection.delete_many({"titel": "Testeintrag"})
print("Gelöschte Dokumente:", loesch_ergebnis.deleted_count)