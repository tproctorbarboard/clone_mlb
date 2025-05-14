# odds/prediction_manager.py
import json
import os

PREDICTION_FILE = "odds/user_predictions.json"

def submit_prediction(gamePk, user, predictions):
    if not os.path.exists("odds"):
        os.makedirs("odds")
    
    if os.path.exists(PREDICTION_FILE):
        with open(PREDICTION_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    if str(gamePk) not in data:
        data[str(gamePk)] = {}

    data[str(gamePk)][user] = predictions

    with open(PREDICTION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_predictions(gamePk):
    if not os.path.exists(PREDICTION_FILE):
        return {}
    with open(PREDICTION_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(gamePk), {})

