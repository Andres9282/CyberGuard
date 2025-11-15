# ml/paths.py
from pathlib import Path

# Directorio raíz del proyecto: .../cyber-shield-ai
ROOT_DIR = Path(__file__).resolve().parents[1]

# Directorio de datos
DATA_DIR = ROOT_DIR / "data"

# Carpeta donde se guardan logs de comportamiento normal
NORMAL_LOG_DIR = DATA_DIR / "logs" / "normal"

# Archivo donde se guardan las muestras de baseline
BASELINE_FILE = DATA_DIR / "baseline_samples.json"

# Ruta al modelo entrenado
MODEL_FILE = ROOT_DIR / "ml" / "model.pkl"
