import os
import requests
from fastapi import FastAPI

app = FastAPI()

API_TOKEN = os.getenv("FOOTBALL_API_KEY")
HEADERS = {"X-Auth-Token": API_TOKEN}

@app.get("/")
def read_root():
    return {"status": "ok", "message": "PitchSignal API is running"}

@app.get("/v1/probability")
def get_probability():
    url = "https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED&limit=1"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        match = data["matches"][0]
        return {
            "fixture_id": match["id"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "score": f"{match['score']['fullTime']['home']}-{match['score']['fullTime']['away']}",
            "source": "football-data.org",
            "status": "live_data"
        }
    except Exception as e:
        return {"error": "Failed to fetch data", "details": str(e)}
