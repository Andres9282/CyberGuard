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
    Recibe eventos enviados por el agente.
    Crea un caso con la evidencia capturada.
    """
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Extraer datos para crear el caso ---
    case_info = {
        "timestamp": timestamp,
        "severity": data.get("severity", "unknown"),
        "process_name": data["evidence"]["process"].get("name", "unknown"),
        "attacker_ip": None,
        "folder": data.get("folder", "unknown"),
        "actions": data.get("actions", [])
    }

    # --- Intentar obtener IP del atacante ---
    try:
        conns = data["evidence"]["network"]
        for c in conns:
            if c.get("raddr"):
                case_info["attacker_ip"] = c["raddr"].split(":")[0]
                break
    except:
        pass

    # Crear caso en DB
    case_id = create_case(case_info)

    # --- Guardar evento ---
    add_event(case_id, {
        "timestamp": timestamp,
        "type": data.get("type", "unknown"),
        "details": data.get("features", {})
    })

    # --- Guardar la evidencia completa ---
    add_evidence(case_id, data["evidence"])

    return jsonify({
        "status": "ok",
        "case_id": case_id,
        "message": "Evento recibido y caso creado exitosamente."
    })


@app.route("/cases", methods=["GET"])
def list_cases():
    """
    Devuelve una lista de todos los casos registrados.
    """
    rows = get_cases()
    return jsonify(rows)


@app.route("/cases/<int:case_id>", methods=["GET"])
def case_details(case_id):
    """
    Devuelve todos los detalles de un caso:
    - datos del caso
    - eventos relacionados
    - evidencia asociada
    """
    return jsonify(get_case_details(case_id))


if __name__ == "__main__":
    # Importante para que otras computadoras puedan conectarse
    app.run(host="0.0.0.0", port=5001)
