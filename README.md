# Stellenmarkt-Pipeline: Data-Analyst-Jobs aus der JSearch-API in MongoDB

Kursprojekt aus meiner Data-Analyst-Weiterbildung am Data Science Institute.
Ein Python-Skript ruft aktuelle Stellenanzeigen für Data Analysts in fünf deutschen
Städten über die JSearch-API (RapidAPI) ab und speichert sie in MongoDB Atlas.
Weitere Skripte prüfen die Datenqualität und werten den Bestand aus.

## Ablauf

| Schritt | Skript | Was passiert |
|---|---|---|
| 1 | `verbindung.py` | Testet die Verbindung zu MongoDB Atlas: Ping, Testdokument einfügen, lesen und wieder löschen |
| 2 | `daten_abrufen.py` | Fragt die API für Berlin, München, Hamburg, Frankfurt und Karlsruhe ab (Vollzeit, je 2 Ergebnisseiten), übernimmt die relevanten Felder und speichert jede Stelle per Upsert auf `job_id` |
| 3 | `qualitaetscheck.py` | Zählt die Dokumente gesamt und pro Stadt und prüft, ob jede `job_id` nur einmal vorkommt |
| 4 | `analyse.py` | Auswertungen: Stellen pro Stadt, Mindestgehalt über 50.000, „Manager“ im Titel, Top 5 Arbeitgeber per Aggregation, Remote gegen vor Ort |
| optional | `aufraeumen.py` | **Löscht alle Dokumente der Collection** ohne Rückfrage. Nur für einen kompletten Neustart gedacht. |

## Warum Upsert

Läuft der Abruf mehrmals, liefert die API teilweise dieselben Stellen erneut.
`update_one(..., upsert=True)` mit `job_id` als Schlüssel aktualisiert eine bekannte
Stelle, statt sie ein zweites Mal anzulegen. Ob das funktioniert hat, prüft
`qualitaetscheck.py`: Die Zahl der eindeutigen `job_id` muss der Zahl der Dokumente entsprechen.

## Gespeicherte Felder

`job_id`, `job_title`, `employer_name`, `job_is_remote`, `job_posted_at`,
`job_location`, `job_salary`, `job_min_salary`, `job_max_salary`,
`job_salary_period`, `job_highlights` sowie `gesuchte_stadt` als eigenes Feld,
damit sich die Ergebnisse später nach der Suchstadt filtern lassen.

## Selbst ausführen

1. Abhängigkeiten installieren: `pip install -r requirements.txt`
2. `.env.example` in `.env` umbenennen und eigene Zugangsdaten eintragen
   (MongoDB-Connection-String und RapidAPI-Schlüssel für JSearch)
3. Skripte in der Reihenfolge der Tabelle oben starten, z. B. `python daten_abrufen.py`

Die `.env` mit den echten Zugangsdaten ist über `.gitignore` vom Repository ausgeschlossen.
Im Code werden sie ausschließlich über `os.getenv()` gelesen.

## Mögliche Erweiterungen

- Statuscode der API prüfen und Fehler abfangen, statt bei einer fehlerhaften Antwort abzubrechen
- Städteliste an einer zentralen Stelle pflegen, sie steht derzeit in zwei Skripten
- Verbindungsaufbau in eine gemeinsame Funktion auslagern
- Abruf zeitgesteuert wiederholen, um die Entwicklung des Stellenmarkts über Wochen zu verfolgen

## Werkzeuge

Python (requests, pymongo, python-dotenv), JSearch-API über RapidAPI, MongoDB Atlas
