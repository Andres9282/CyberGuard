from flask import Flask, request, jsonify
from flask_cors import CORS
from db_locall import create_tables, create_case, add_event, add_artifact, get_cases, get_case_details

app = Flask(__name__)
CORS(app)

create_tables()  # Crear tablas al iniciar backend


@app.route("/event", methods=["POST"])
def receive_event():
    data = request.json

    # 1. Crear caso
    case_id = create_case(data)

    # 2. Guardar eventos internos
    for ev in data.get("events", []):
        ev["timestamp"] = data.get("timestamp")
        add_event(case_id, ev)

    # 3. Guardar artefactos (evidencias)
    for art in data.get("artifacts", []):
        add_artifact(case_id, art)

    return jsonify({"status": "ok", "case_id": case_id})


@app.route("/cases", methods=["GET"])
def list_cases():
    return jsonify(get_cases())


@app.route("/cases/<int:case_id>", methods=["GET"])
def case_details(case_id):
    return jsonify(get_case_details(case_id))

@app.route("/", methods=["GET"])
def home():
    return "<h1 style='font-size:60px; color:purple;'>¡¡VAMOSSSSSSSSSSSSSSSSSSSSSSSSS!! 🔥🔥🔥</h1>"
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "backend listo 🔥",
        "message": "Todo funcionando VAMOSSSSSSSSSSS 💪",
        "ok": True
    })

if __name__ == "__main__":
    app.run(port=5001, debug=True)

