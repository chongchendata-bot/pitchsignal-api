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
    # 改做拎「即將舉行」嘅比賽，咁就一定有數據
    url = "https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED&limit=1"
    
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        # 防錯誤：先檢查有冇 matches
        if not data.get("matches"):
            return {"error": "No scheduled matches found", "raw_response": data}
            
        match = data["matches"][0]
        
        return {
            "fixture_id": match["id"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "kickoff": match["utcDate"],
            "source": "football-data.org",
            "status": "live_data"
        }
    except Exception as e:
        return {"error": "Failed to fetch data", "details": str(e)}
