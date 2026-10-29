# Stellen über JSearch (RapidAPI) holen und in MongoDB speichern

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests

load_dotenv()

url = "https://jsearch.p.rapidapi.com/search-v2"


# Key und URI nur aus der .env, nicht hier reinschreiben!
mongo_uri = os.getenv("MONGO_URI")
api_key = os.getenv("RAPIDAPI_KEY")

client = MongoClient(mongo_uri)
db = client["jobsearch"]
collection = db["offene_stellen"]

headers = {
    "x-rapidapi-host": "jsearch.p.rapidapi.com",
    "x-rapidapi-key": api_key
}



staedte = ["Berlin", "München", "Hamburg", "Frankfurt", "Karlsruhe"]

for stadt in staedte:
    querystring = {
        "query": f"Data Analyst jobs in {stadt}",
        "country": "de",
        "num_pages": "2",               # 2 Seiten pro Stadt reichen erstmal
        "employment_types": "FULLTIME"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(stadt, response.status_code)  # 200 = ok

    # TODO: bei Fehler (z.B. 429 Limit) bricht es hier ab, Statuscode vorher abfragen
    daten = response.json()
    jobs = daten["data"]["jobs"]

    for job in jobs:
        # nur die Felder, die ich brauche - die API schickt viel mehr mit
        # .get() damit es nicht knallt, wenn mal ein Feld fehlt
        gefilterter_job = {
            "job_id": job.get("job_id"),
            "job_title": job.get("job_title"),
            "employer_name": job.get("employer_name"),
            "job_is_remote": job.get("job_is_remote"),
            "job_posted_at": job.get("job_posted_at"),
            "job_location": job.get("job_location"),
            "job_salary": job.get("job_salary"),
            "job_min_salary": job.get("job_min_salary"),
            "job_max_salary": job.get("job_max_salary"),
            "job_salary_period": job.get("job_salary_period"),
            "job_highlights": job.get("job_highlights"),
            "gesuchte_stadt": stadt   # selbst ergänzt, zum Filtern nach Stadt
        }

        # upsert statt insert: gleiche job_id wird überschrieben, nicht doppelt angelegt
        # -> Skript kann ich beliebig oft laufen lassen
        collection.update_one(
            {"job_id": gefilterter_job["job_id"]},
            {"$set": gefilterter_job},
            upsert=True
        )
