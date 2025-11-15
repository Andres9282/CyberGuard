import joblib
import numpy as np

model = joblib.load("ml/model.joblib")

def predict_event(features):
    vec = np.array([
        features.get("size_change", 0),
        features.get("created", 0),
        features.get("deleted", 0),
        features.get("entropy", 0),
        features.get("rapid_changes", 0)
    ]).reshape(1, -1)

    pred = model.predict(vec)[0]
    return "attack" if pred == 1 else "normal"
