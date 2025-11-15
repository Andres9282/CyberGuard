# backend/server.py
from flask import Flask, request, jsonify
from datetime import datetime
import subprocess

from db import (
    create_tables, create_case, add_event,
    add_evidence, get_cases, get_case_details
)

app = Flask(__name__)

# Crear tablas al iniciar
create_tables()


# ============================================
#  INDEX
# ============================================
@app.route("/")
def index():
    return "CyberGuard Backend OK"


# ============================================
#  RECIBIR EVENTO DEL AGENTE
# ============================================
@app.route("/event", methods=["POST"])
def receive_event():
    """
    Recibe eventos del agente.
    Maneja JSON incompleto sin romper el servidor.
    """

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -------------------------
    # 1) Extraer evidencia con seguridad
    # -------------------------
    evidence = data.get("evidence", {})
    process_info = evidence.get("process", {})
    network_info = evidence.get("network", [])
    files_info = evidence.get("files", [])

    # -------------------------
    # 2) Crear objeto para BD
    # -------------------------
    case_info = {
        "timestamp": timestamp,
        "severity": data.get("severity", "unknown"),
        "process_name": process_info.get("name", "unknown"),
        "attacker_ip": None,
        "folder": data.get("folder", "unknown"),
        "actions": data.get("actions", [])
    }

    # -------------------------
    # 3) Intentar capturar IP atacante
    # -------------------------
    try:
        for c in network_info:
            if isinstance(c, dict) and c.get("raddr"):
                case_info["attacker_ip"] = c["raddr"].split(":")[0]
                break
    except Exception as e:
        print("Error analizando conexiones:", e)

    # -------------------------
    # 4) Insertar caso en BD
    # -------------------------
    try:
        case_id = create_case(case_info)
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    # -------------------------
    # 5) Registrar evento del caso
    # -------------------------
    add_event(case_id, {
        "timestamp": timestamp,
        "type": data.get("type", "unknown"),
        "details": data.get("features", {})
    })

    # -------------------------
    # 6) Guardar evidencia
    # -------------------------
    add_evidence(case_id, {
        "process": process_info,
        "network": network_info,
        "files": files_info,
        "path_triggered": evidence.get("path_triggered", "")
    })

    return jsonify({
        "status": "ok",
        "case_id": case_id,
        "message": "Evento recibido correctamente."
    })


# ============================================
# LISTAR CASOS
# ============================================
@app.route("/cases", methods=["GET"])
def list_cases():
    rows = get_cases()
    return jsonify(rows)


# ============================================
# OBTENER DETALLES DE UN CASO
# ============================================
@app.route("/cases/<int:case_id>", methods=["GET"])
def case_details(case_id):
    return jsonify(get_case_details(case_id))


# ============================================
# EJECUTAR ATAQUE REMOTO (desde otra PC)
# ============================================
@app.route("/run_attack", methods=["POST"])
def run_attack():
    """
    Endpoint que permite disparar un ataque simulado dentro de WSL.
    El atacante lo llama vía POST desde otra computadora.
    """
    data = request.get_json(silent=True)
    action = data.get("action", "")

    if action != "encrypt":
        return jsonify({"error": "Acción no válida"}), 400

    try:
        subprocess.Popen(
            ["python3", "attack/attack_simulated.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return jsonify({"status": "ok", "message": "Ataque simulado iniciado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# RUN SERVER
# ============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
