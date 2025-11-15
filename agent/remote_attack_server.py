# agent/remote_attack_server.py
# Servidor que recibe comandos de ataque remoto desde otra computadora

import os
import sys
import subprocess
from flask import Flask, request, jsonify
import threading
from pathlib import Path

# CORS opcional
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False

# Importar configuración
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from backend.config import AGENT_HOST, AGENT_PORT, FOLDER_TO_WATCH

app = Flask(__name__)
if CORS_AVAILABLE:
    CORS(app)

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "service": "CyberGuard Remote Attack Server",
        "port": AGENT_PORT,
        "watch_folder": FOLDER_TO_WATCH
    })

@app.route("/attack", methods=["POST"])
def execute_attack():
    """
    Endpoint que recibe comandos de ataque remoto.
    Ejecuta el simulador de ransomware en la computadora objetivo.
    """
    data = request.get_json(silent=True) or {}
    
    # Parámetros del ataque
    target_folder = data.get("target_folder", FOLDER_TO_WATCH)
    num_files = data.get("num_files", 10)
    delay = data.get("delay", 0.1)
    
    print(f"\n🔥 ATAQUE REMOTO RECIBIDO")
    print(f"   Carpeta objetivo: {target_folder}")
    print(f"   Archivos: {num_files}")
    print(f"   Delay: {delay}s")
    
    try:
        # Ejecutar el script de ataque
        script_path = Path(__file__).parent / "ransomware_test.py"
        
        # Ejecutar en un hilo separado para no bloquear
        def run_attack():
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path), target_folder, str(num_files), str(delay)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                print(result.stdout)
                if result.stderr:
                    print(f"Errores: {result.stderr}")
            except Exception as e:
                print(f"Error ejecutando ataque: {e}")
        
        attack_thread = threading.Thread(target=run_attack, daemon=True)
        attack_thread.start()
        
        return jsonify({
            "status": "ok",
            "message": "Ataque iniciado",
            "target_folder": target_folder,
            "num_files": num_files,
            "delay": delay
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/status", methods=["GET"])
def status():
    """Endpoint para verificar el estado del servidor de ataque"""
    return jsonify({
        "status": "running",
        "watch_folder": FOLDER_TO_WATCH,
        "folder_exists": Path(FOLDER_TO_WATCH).exists()
    })

if __name__ == "__main__":
    print(f"🔴 Servidor de Ataque Remoto iniciado")
    print(f"   Host: {AGENT_HOST}")
    print(f"   Port: {AGENT_PORT}")
    print(f"   Carpeta monitoreada: {FOLDER_TO_WATCH}")
    print(f"\n   Para ejecutar un ataque desde otra computadora:")
    print(f"   POST http://<IP_ESTA_COMPUTADORA>:{AGENT_PORT}/attack")
    
    app.run(host=AGENT_HOST, port=AGENT_PORT, debug=False)

