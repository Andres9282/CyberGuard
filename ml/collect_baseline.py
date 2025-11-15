# ml/collect_baseline.py
import time
import json
from pathlib import Path

from .paths import BASELINE_FILE, NORMAL_LOG_DIR
from .features import extract_features


NUM_SAMPLES = 50      # cuántas muestras tomar
SLEEP_SECONDS = 0.3   # tiempo entre muestras


def main():
    # Crear carpeta de logs normales si no existe
    NORMAL_LOG_DIR.mkdir(parents=True, exist_ok=True)

    samples = []
    print("🔵 Recolectando baseline de comportamiento NORMAL...")
    print(f"   Carpeta observada: {NORMAL_LOG_DIR}")
    print(f"   Muestras: {NUM_SAMPLES}, intervalo: {SLEEP_SECONDS} s\n")

    for i in range(NUM_SAMPLES):
        feats = extract_features(NORMAL_LOG_DIR)
        samples.append(feats)
        print(f"Muestra {i+1:02d}: {feats}")
        time.sleep(SLEEP_SECONDS)

    # Crear carpeta data si no existe
    BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with BASELINE_FILE.open("w", encoding="utf-8") as f:
        json.dump(samples, f, indent=4)

    print(f"\n🟢 Baseline guardado en: {BASELINE_FILE}")
    print("   Ahora puedes entrenar el modelo con: python -m ml.train_model")


if __name__ == "__main__":
    main()
