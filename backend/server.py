# backend/server.py
from flask import Flask, request, jsonify
from ml.detect import predict_event    # ML real
from backend.config import BACKEND_HOST, BACKEND_PORT

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "CyberGuard backend funcionando"

@app.route("/event", methods=["POST"])
def receive_event():
    data = request.get_json(silent=True) or {}

    features = data.get("features", {})
    prediction = predict_event(features)

    print("📩 Evento recibido:", data)
    print("🤖 Clasificación ML:", prediction)

    return jsonify({
        "status": "ok",
        "prediction": prediction,
        "received": data
    })

if __name__ == "__main__":
    app.run(host=BACKEND_HOST, port=BACKEND_PORT)
