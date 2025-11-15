# ml/detect.py

import pickle
from pathlib import Path
from ml.features import extract_features   # <-- IMPORTAMOS LA FUNCIÓN UNIFICADA


MODEL_PATH = Path("ml/anomaly_model.pkl")


# ---------------------------------------
# CARGAR MODELO
# ---------------------------------------

def load_model():
    if MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return None


model = load_model()


# ---------------------------------------
# DETECTAR ANOMALÍAS
# ---------------------------------------

def detect_anomaly(features):
    """
    Usa el IsolationForest entrenado para determinar si hay anomalía.
    Retorna True si es ataque.
    """
    if model is None:
        print("⚠️ Modelo no cargado → no se detectan anomalías.")
        return False

    try:
        prediction = model.predict([features])[0]
        return prediction == -1  # -1 = anomalía
    except Exception as e:
        print("ERROR detectando anomalía:", e)
        return False


# ---------------------------------------
# MODO PRUEBA: evaluar estado actual en tiempo real
# ---------------------------------------

def detect_live():
    features = extract_features()
    print("Features recolectados ahora:", features)
    return detect_anomaly(features)


if __name__ == "__main__":
    print("🔍 Prueba rápida de detección en vivo:")
    result = detect_live()
    print("¿Ataque detectado?:", result)
