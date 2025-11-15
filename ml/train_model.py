# ml/train_model.py
import json
import numpy as np
import pickle
from sklearn.ensemble import IsolationForest
from .paths import BASELINE_FILE, MODEL_FILE


def load_baseline():
    if not BASELINE_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de baseline: {BASELINE_FILE}\n"
            f"Primero ejecuta: python -m ml.collect_baseline"
        )
    with BASELINE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    X = np.array(data, dtype=float)
    if X.ndim != 2 or X.shape[0] < 10:
        raise ValueError(
            f"El baseline es insuficiente o tiene formato incorrecto. "
            f"Se necesitan al menos 10 muestras. Actual: {X.shape}"
        )
    return X


def train_model(X):
    model = IsolationForest(
        contamination=0.1,   # un poco más relajado
        n_estimators=100,
        random_state=42
    )
    model.fit(X)
    return model


def main():
    print("🔵 Cargando baseline...")
    X = load_baseline()
    print(f"   Muestras cargadas: {X.shape[0]}, features por muestra: {X.shape[1]}")

    print("🔵 Entrenando Isolation Forest...")
    model = train_model(X)

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_FILE.open("wb") as f:
        pickle.dump(model, f)

    print(f"🟢 Modelo entrenado y guardado en: {MODEL_FILE}")
    print("   Ahora puedes usarlo desde ml.detect.detect_anomaly(features)")


if __name__ == "__main__":
    main()
