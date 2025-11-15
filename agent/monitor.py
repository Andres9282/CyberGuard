import time
import requests
import hashlib
from pathlib import Path
from datetime import datetime
from ml.features import extract_features
from ml.detect import predict_event

# ==============================
# CONFIGURACIÓN
# ==============================

WATCH_FOLDER = r"C:\attack_test"      # Carpeta que se monitorea
BACKEND_URL = "http://100.82.42.122:5001/event"   # PC1 via Tailscale

SCAN_INTERVAL = 1.5   # segundos
STOP_ON_DETECTION = True


# ==============================
# FUNCIONES DE APOYO
# ==============================

def calculate_hash(path):
    """Devuelve hash SHA256 de un archivo."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None


def get_artifacts(folder):
    """Recolecta archivos nuevos/modificados como evidencia."""
    artifacts = []

    folder = Path(folder)
    for file in folder.glob("*"):
        if file.is_file():
            artifacts.append({
                "path": str(file),
                "hash": calculate_hash(file),
                "op": "modified"
            })
    return artifacts


def send_event(process_name, attacker_ip, artifacts):
    """Envía un evento REAL al backend (dashboard)."""

    features = extract_features(WATCH_FOLDER)
    severity = predict_event(features)

    payload = {
        "timestamp": datetime.now().isoformat(),
        "severity": severity,
        "process_name": process_name,
        "attacker_ip": attacker_ip,
        "attack_type": "ransomware",
        "actions": ["process_terminated"] if severity != "normal" else [],

        "events": [
            {
                "timestamp": datetime.now().isoformat(),
                "event_type": "ml_detection",
                "details": features
            }
        ],

        "artifacts": [
            {
                "file_path": art["path"],
                "hash": art["hash"],
                "operation": art["op"]
            }
            for art in artifacts
        ]
    }

    print("\n📤 Enviando evento al backend…")
    try:
        r = requests.post(BACKEND_URL, json=payload, timeout=5)
        print("📥 Respuesta del backend:", r.text)
    except Exception as e:
        print("❌ Error enviando evento:", e)

    return severity


# ==============================
# MONITOR PRINCIPAL
# ==============================

def run_monitor():
    print("🟦 CYBERGUARD MONITOR INICIADO")
    print(f"📁 Carpeta: {WATCH_FOLDER}")
    print(f"🛰 Enviando datos a backend: {BACKEND_URL}\n")

    last_state = {}

    while True:
        try:
            artifacts = get_artifacts(WATCH_FOLDER)
            features = extract_features(WATCH_FOLDER)

            # Revisar si hay cambios significativos = potencial ataque
            if features["rapid_changes"] > 10 or features["encrypted"] > 3:
                print("\n🚨 ALERTA: Actividad sospechosa detectada")
                print(f"🔎 Features: {features}")

                severity = send_event(
                    process_name="python_monitor",
                    attacker_ip="100.99.233.46",  # IP de PC2 por Tailscale
                    artifacts=artifacts
                )

                if severity != "normal":
                    print("\n🛑 RANSOMWARE DETECTADO")
                    print("❌ Monitor DETENIDO para evitar más daño")
                    print("⚠ Revisa el Dashboard en PC1\n")

                    if STOP_ON_DETECTION:
                        return  # 🔥 Detiene el monitor completamente

            time.sleep(SCAN_INTERVAL)

        except KeyboardInterrupt:
            print("\n🟡 Monitor detenido manualmente.")
            return
        except Exception as e:
            print("❌ Error en monitor:", e)
            time.sleep(2)


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    run_monitor()
