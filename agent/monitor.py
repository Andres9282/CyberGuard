from ml.features import extract_features
from ml.detect import detect_anomaly

MONITOR_FOLDER = "data/logs/attack"  # por ejemplo

while True:
    features = extract_features(MONITOR_FOLDER)
    if detect_anomaly(features):
        # 1. Ejecutar acciones de defensa (kill, lock, etc.)
        # 2. Enviar evento al backend vía POST /event
    time.sleep(0.3)
