# ein paar Auswertungen auf dem Bestand

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["jobsearch"]
collection = db["offene_stellen"]

gesamt = collection.count_documents({})
print("Gesamtanzahl Jobs:", gesamt)

berlin_jobs = collection.count_documents({"gesuchte_stadt": "Berlin"})
print("Jobs in Berlin:", berlin_jobs)

# $gt = größer als
# Achtung: viele Anzeigen haben gar kein Gehalt drin, die Zahl ist also eher zu niedrig
gut_bezahlte_jobs = collection.count_documents({"job_min_salary": {"$gt": 50000}})
print("Jobs mit Mindestgehalt über 50.000:", gut_bezahlte_jobs)

# "i" -> Groß-/Kleinschreibung egal
manager_jobs = collection.count_documents({"job_title": {"$regex": "Manager", "$options": "i"}})
print("Jobs mit 'Manager' im Titel:", manager_jobs)

# gruppieren nach Firma, zählen, sortieren, Top 5
top_unternehmen = collection.aggregate([
    {"$group": {"_id": "$employer_name", "anzahl": {"$sum": 1}}},
    {"$sort": {"anzahl": -1}},
    {"$limit": 5}
])

print("Top 5 Unternehmen:")
for eintrag in top_unternehmen:
    print(eintrag["_id"], ":", eintrag["anzahl"], "Jobs")


remote_jobs = collection.count_documents({"job_is_remote": True})
vor_ort_jobs = collection.count_documents({"job_is_remote": False})
print("Remote Jobs:", remote_jobs)
print("Vor-Ort Jobs:", vor_ort_jobs)
