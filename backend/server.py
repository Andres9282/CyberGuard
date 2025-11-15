# backend/server.py
from flask import Flask, request, jsonify
from datetime import datetime
from backend.db import (
    create_tables, create_case, add_event,
    add_evidence, get_cases, get_case_details
)
from backend.config import BACKEND_HOST, BACKEND_PORT, AGENT_ATTACK_URL
from backend.reports.report_builder import build_case_report
import requests

app = Flask(__name__)

# Crear tablas al iniciar
create_tables()

@app.route("/")
def index():
    return "CyberGuard Backend OK"


@app.route("/event", methods=["POST"])
def receive_event():
    """
    Recibe eventos del agente.
    Crea un caso y maneja JSON incompleto sin fallar.
    """

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -------------------------
    # 1) Extraer evidencia segura
    # -------------------------

    evidence = data.get("evidence", {})
    process_info = evidence.get("process", {})
    network_info = evidence.get("network", [])
    files_info = evidence.get("files", [])

    # -------------------------
    # 2) Construir caso
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
    # 3) Intentar obtener la IP del atacante
    # -------------------------

    try:
        for c in network_info:
            if isinstance(c, dict) and c.get("raddr"):
                case_info["attacker_ip"] = c["raddr"].split(":")[0]
                break
    except Exception as e:
        print("Error analizando conexiones:", e)

    # -------------------------
    # 4) Crear caso en base de datos
    # -------------------------

    try:
        case_id = create_case(case_info)
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    # -------------------------
    # 5) Guardar evento
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


@app.route("/cases", methods=["GET"])
def list_cases():
    rows = get_cases()
    return jsonify(rows)


@app.route("/cases/<int:case_id>", methods=["GET"])
def case_details(case_id):
    return jsonify(get_case_details(case_id))


@app.route("/report/<int:case_id>")
def report(case_id):
    data = get_case_details(case_id)
    html = build_case_report(
        data["case"],
        data["events"],
        data["evidence"]
    )
    return html


@app.route("/trigger-attack", methods=["POST"])
def trigger_remote_attack():
    """
    Endpoint para disparar un ataque remoto desde otra computadora.
    Este endpoint recibe la solicitud y la reenvía al agente en la computadora objetivo.
    """
    data = request.get_json(silent=True) or {}
    
    # Parámetros del ataque
    agent_ip = data.get("agent_ip")
    agent_port = data.get("agent_port", 5002)
    target_folder = data.get("target_folder")
    num_files = data.get("num_files", 10)
    delay = data.get("delay", 0.1)
    
    if not agent_ip:
        return jsonify({
            "status": "error",
            "message": "Se requiere 'agent_ip' para ejecutar ataque remoto"
        }), 400
    
    attack_url = f"http://{agent_ip}:{agent_port}/attack"
    payload = {
        "num_files": num_files,
        "delay": delay
    }
    
    if target_folder:
        payload["target_folder"] = target_folder
    
    try:
        print(f"🔴 Reenviando comando de ataque a {agent_ip}:{agent_port}")
        response = requests.post(attack_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        return jsonify({
            "status": "ok",
            "message": "Ataque remoto iniciado exitosamente",
            "agent_response": result
        })
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": "error",
            "message": f"No se pudo conectar al agente en {agent_ip}:{agent_port}. Verifica que el servidor de ataque esté ejecutándose."
        }), 503
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error ejecutando ataque remoto: {str(e)}"
        }), 500


if __name__ == "__main__":
    print(f"🔵 CyberGuard Backend iniciado")
    print(f"   Host: {BACKEND_HOST}")
    print(f"   Port: {BACKEND_PORT}")
    app.run(host=BACKEND_HOST, port=BACKEND_PORT)
