# ml/detect.py
import joblib
import numpy as np

MODEL_PATH = "ml/model.joblib"

try:
    model = joblib.load(MODEL_PATH)
except:
    model = None
    print("⚠ Modelo ML no encontrado. Solo modo debug.")

def predict_event(features: dict):
    if model is None:
        return "unknown"

    vector = np.array([features.get("size_change", 0),
                       features.get("created", 0),
                       features.get("deleted", 0),
                       features.get("encrypted", 0),
                       features.get("rapid_changes", 0)]).reshape(1, -1)

    pred = model.predict(vector)[0]
    return "attack" if pred == 1 else "normal"
