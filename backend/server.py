# backend/server.py
from flask import Flask, request, jsonify
from datetime import datetime

from backend.db import (
    create_tables, create_case, add_event,
    add_evidence, get_cases, get_case_details
)

from backend.reports.report_builder import build_case_report

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
    data = request.json
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    case_info = {
        "timestamp": timestamp,
        "severity": data.get("severity", "unknown"),
        "process_name": process_info.get("name", "unknown"),
        "attacker_ip": None,
        "folder": data.get("folder", "unknown"),
        "actions": data.get("actions", [])
    }

    try:
        for c in network_info:
            if isinstance(c, dict) and c.get("raddr"):
                case_info["attacker_ip"] = c["raddr"].split(":")[0]
                break
    except Exception as e:
        print("Error analizando conexiones:", e)

    case_id = create_case(case_info)

    add_event(case_id, {
        "timestamp": timestamp,
        "type": data.get("type", "unknown"),
        "details": data.get("features", {})
    })

    add_evidence(case_id, data["evidence"])

    return jsonify({"status": "ok", "case_id": case_id})


@app.route("/cases")
def list_cases():
    return jsonify(get_cases())


@app.route("/cases/<int:case_id>")
def case_details(case_id):
    return jsonify(get_case_details(case_id))


# 🚨 ESTA ES LA RUTA DEL REPORTE (ya corregida)
@app.route("/report/<int:case_id>")
def report(case_id):
    data = get_case_details(case_id)
    html = build_case_report(
        data["case"],
        data["events"],
        data["evidence"]
    )
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
