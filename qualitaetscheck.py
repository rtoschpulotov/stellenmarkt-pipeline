import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["jobsearch"]
collection = db["offene_stellen"]

gesamt = collection.count_documents({})
print("Gesamtanzahl Dokumente:", gesamt)

staedte = ["Berlin", "München", "Hamburg", "Frankfurt", "Karlsruhe"]

for stadt in staedte:
    anzahl = collection.count_documents({"gesuchte_stadt": stadt})
    print(stadt, ":", anzahl, "Jobs")

alle_job_ids = [dokument["job_id"] for dokument in collection.find({}, {"job_id": 1})]
anzahl_eindeutig = len(set(alle_job_ids))
anzahl_gesamt = len(alle_job_ids)

print("Eindeutige job_ids:", anzahl_eindeutig, "von", anzahl_gesamt, "Dokumenten")