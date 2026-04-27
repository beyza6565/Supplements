from fastapi import FastAPI
import csv
import os

app = FastAPI()

# Das hier ist aus Aufgabe 5 gefordert!
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def get_metrics():
    # Wir suchen nach deiner Datei
    file_path = "data/zeitverlauf.csv"
    if not os.path.exists(file_path):
        file_path = "../data/zeitverlauf.csv"

    if not os.path.exists(file_path):
        return {"error": "Datei 'zeitverlauf.csv' nicht gefunden. Prüfe den Namen im Ordner 'data'."}

    results = []
    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file))

            # 1. Finde die Zeile, wo die Daten wirklich anfangen
            start_line = 0
            for i, row in enumerate(reader):
                if row and any(key in row[0] for key in ["Woche", "Monat", "Zeit", "Time"]):
                    start_line = i
                    break

            headers = reader[start_line]
            terms = headers[1:] # Alles außer der Zeit-Spalte

            data_map = {term: [] for term in terms}

            # 2. Daten sammeln und bereinigen
            for row in reader[start_line + 1:]:
                if not row or len(row) < len(headers):
                    continue

                for i, term in enumerate(terms):
                    val = row[i + 1]
                    if val == "<1":
                        val = 0
                    try:
                        data_map[term].append(int(val))
                    except ValueError:
                        continue

            # 3. Kennzahlen berechnen
            for term in terms:
                vals = data_map[term]
                if not vals:
                    continue

                mean_val = sum(vals) / len(vals)
                peak_val = max(vals)

                first, last = vals[0], vals[-1]
                trend = "increasing" if last > first else "decreasing" if last < first else "stable"

                results.append({
                    "name": term,
                    "mean": round(mean_val, 1),
                    "peak": peak_val,
                    "trend": trend
                })

        return {"terms": results}
    except Exception as e:
        return {"error": str(e)}