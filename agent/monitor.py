# agent/monitor.py

import time
import json
import psutil
import requests
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ml.detect import detect_anomaly
from ml.features import extract_features   # <-- USAMOS LA FUNCIÓN NUEVA UNIFICADA


# ------------------------------
# CONFIGURACIÓN DEL AGENTE
# ------------------------------

FOLDER_TO_WATCH = "/home/andres/attack_test"   # Carpeta vulnerable
BACKEND_URL = "http://10.74.10.88:5001/event"  # IP real de Windows (WSL expuesto)
COOLDOWN_SECONDS = 5
last_trigger_time = 0


# ------------------------------
# FUNCIÓN: Extraer evidencia
# ------------------------------

def collect_evidence(path_changed):
    # 1. top proceso por uso de CPU
    suspicious = sorted(
        psutil.process_iter(['pid', 'name', 'cpu_percent']),
        key=lambda p: p.info['cpu_percent'],
        reverse=True
    )
    top_process = suspicious[0].info if suspicious else {"name": "unknown", "pid": -1}

    # 2. conexiones de red
    conns = []
    for c in psutil.net_connections():
        try:
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else None
            conns.append({"pid": c.pid, "laddr": str(c.laddr), "raddr": raddr})
        except:
            pass

    # 3. archivos en carpeta monitoreada
    files = []
    for p in Path(FOLDER_TO_WATCH).glob("**/*"):
        if p.is_file():
            files.append(str(p))

    return {
        "process": top_process,
        "network": conns,
        "files": files,
        "path_triggered": path_changed
    }


# ------------------------------
# FUNCIÓN: DETENER ATAQUE
# ------------------------------

def stop_attack(process_name):
    killed = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()
                killed.append(proc.info)
        except:
            pass
    return killed


# ------------------------------
# FUNCIÓN: ENVIAR REPORTE
# ------------------------------

def send_to_backend(severity, features, evidence, actions, folder):
    data = {
        "severity": severity,
        "type": "filesystem_anomaly",
        "folder": folder,
        "features": features,
        "actions": actions,
        "evidence": evidence
    }
    try:
        res = requests.post(BACKEND_URL, json=data)
        print(" Enviado a backend →", res.text)
    except Exception as e:
        print(" Error enviando al backend:", e)


# ------------------------------
# HANDLER: DETECTA CAMBIOS
# ------------------------------

class FolderChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global last_trigger_time

        now = time.time()
        if now - last_trigger_time < COOLDOWN_SECONDS:
            return

        last_trigger_time = now

        print("\n⚠️ Cambio detectado:", event.src_path)

        # 1. EXTRAER FEATURES (la misma función que baseline)
        features = extract_features(FOLDER_TO_WATCH)
        print("Features extraídos:", features)

        # 2. IA detecta ataque
        is_attack = detect_anomaly(features)
        if not is_attack:
            print("📘 No es ataque. Comportamiento normal.")
            return

        print("🔥 ATAQUE DETECTADO: posible ransomware")

        # 3. recolectar evidencia
        evidence = collect_evidence(event.src_path)

        # 4. parar proceso sospechoso
        killed = stop_attack(evidence["process"]["name"])
        actions = {"killed_processes": killed}

        # 5. enviar reporte
        send_to_backend(
            severity="high",
            features=features,
            evidence=evidence,
            actions=actions,
            folder=FOLDER_TO_WATCH
        )


# ------------------------------
# MAIN
# ------------------------------

if __name__ == "__main__":
    print("🔵 CyberGuard Agent iniciado...")
    print(f"Vigilando: {FOLDER_TO_WATCH}")
    handler = FolderChangeHandler()
    observer = Observer()
    observer.schedule(handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
