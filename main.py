import os
import requests
import numpy as np
from fastapi import FastAPI

app = FastAPI()

API_TOKEN = os.getenv("FOOTBALL_API_KEY")
HEADERS = {"X-Auth-Token": API_TOKEN}

# --- 简易泊松模型 (模拟 Elo/xG 转化来的主胜概率) ---
HOME_ATTACK = 1.8
AWAY_DEFENSE = 1.2
EXPECTED_GOALS_HOME = HOME_ATTACK * AWAY_DEFENSE
MODEL_HOME_WIN_PROB = np.exp(-EXPECTED_GOALS_HOME) * (1 + EXPECTED_GOALS_HOME + (EXPECTED_GOALS_HOME**2)/2)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "PitchSignal API is running with Mispricing Signal"}

@app.get("/v1/probability")
def get_probability():
    url = "https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED&limit=1"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if not data.get("matches"):
            return {"error": "No scheduled matches found", "raw_response": data}
        match = data["matches"][0]
        MARKET_HOME_WIN_PROB = 0.55 
        deviation = MODEL_HOME_WIN_PROB - MARKET_HOME_WIN_PROB
        return {
            "fixture_id": match["id"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "source": "football-data.org + Poisson Model",
            "status": "live_signal",
            "model_probability": round(MODEL_HOME_WIN_PROB, 4),
            "market_probability": MARKET_HOME_WIN_PROB,
            "deviation_z": round(deviation, 4),
            "signal": "BUY HOME" if deviation > 0.03 else "NO EDGE"
        }
    except Exception as e:
        return {"error": "Failed to fetch data", "details": str(e)}
