from fastapi import FastAPI
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv

# Lädt den geheimen Key aus der .env Datei
load_dotenv()

app = FastAPI()

# Wir konfigurieren den Client so, dass er deinen Deepseek-Key nutzt
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analyze")
def analyze_trends():
    # 1. Daten über HTTP vom Data-Service abfragen (genau wie gefordert!)
    # Falls er in Docker läuft, sucht er unter "data-service", sonst lokal unter "localhost"
    url = os.getenv("DATA_SERVICE_URL", "http://localhost:8000/metrics")

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return {"error": "Konnte Data-Service nicht erreichen.", "details": str(e)}

    # 2. Den perfekten Prompt für den Dozenten bauen
    prompt = f"""
    Du bist ein Datenanalyst. Hier sind die Google Trends Daten für verschiedene Supplements der letzten 30 Tage in Deutschland:
    {data}

    Erstelle eine kurze, strukturierte Interpretation basierend auf diesen Kennzahlen (Mean, Peak, Trend).
    Beantworte dabei zwingend diese drei Fragen:
    1. Welcher Begriff zeigt den stärksten Trend?
    2. Wo treten die höchsten Peaks auf?
    3. Welche wesentlichen Unterschiede gibt es zwischen den Begriffen?
    """

    # 3. Deepseek KI um eine Antwort bitten
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Du bist ein präziser, sachlicher Datenanalyst."},
                {"role": "user", "content": prompt}
            ],
            model="deepseek-chat",
        )
        return {
            "source_data": data, # Wir zeigen dem Prof, dass die Daten da sind
            "ai_interpretation": chat_completion.choices[0].message.content
        }
    except Exception as e:
        return {"error": str(e)}