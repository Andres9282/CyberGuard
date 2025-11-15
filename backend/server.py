# backend/server.py
from flask import Flask, request, jsonify
from datetime import datetime
from db import (
    create_tables, create_case, add_event,
    add_evidence, get_cases, get_case_details
)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
