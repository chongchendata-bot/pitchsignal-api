from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "PitchSignal API is running"}

@app.get("/v1/probability")
def get_probability():
    # 呢度將來會放你嘅足球概率模型
    return {
        "fixture_id": 88293,
        "market": "win_draw_win",
        "model_probability": {
            "home_win": 0.473,
            "draw": 0.261,
            "away_win": 0.266
        },
        "source": "xg_sync_v1"
    }
