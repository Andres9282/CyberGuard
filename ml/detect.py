# ml/detect.py

import json
import psutil
import pickle
from pathlib import Path

MODEL_PATH = Path("ml/anomaly_model.pkl")
BASELINE_PATH = Path("data/baseline_samples.json")


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
# EXTRAER FEATURES PARA EL MODELO ML
# ---------------------------------------

def extract_features_for_ml():
    """
    Extrae métricas del sistema:
    - número de procesos
    - uso de CPU promedio
    - uso de RAM
    """
    processes = list(psutil.process_iter())
    num_processes = len(processes)

    cpu_percent = psutil.cpu_percent(interval=0.2)
    ram_percent = psutil.virtual_memory().percent

    return [num_processes, cpu_percent, ram_percent]


# ---------------------------------------
# DETECTAR ANOMALÍAS
# ---------------------------------------

def detect_anomaly(features):
    """
    Usa el modelo entrenado para detectar anomalías.
    Si no hay modelo → siempre retorna False.
    """
    if model is None:
        print("⚠️ Modelo no cargado → no se detectan anomalías.")
        return False

    try:
        prediction = model.predict([features])[0]
        # IsolationForest: -1 = anomalía, 1 = normal
        return prediction == -1
    except Exception as e:
        print("ERROR detectando anomalía:", e)
        return False
