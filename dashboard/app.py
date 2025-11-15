from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)
BACKEND_URL = "http://localhost:8000"  # Tu backend real

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Estado básico del sistema - ESENCIAL"""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "status": "ERROR", 
                "message": f"Backend respondió con error: {response.status_code}",
                "last_update": datetime.now().isoformat()
            })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "ESCUDO", 
            "message": f"No se puede conectar al backend: {str(e)}",
            "last_update": datetime.now().isoformat()
        })

@app.route('/api/cases')
def get_cases():
    """Lista de casos - ESENCIAL"""
    try:
        response = requests.get(f"{BACKEND_URL}/cases", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error del backend: {response.status_code}", "cases": []})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión: {str(e)}", "cases": []})

@app.route('/api/cases/<case_id>')
def get_case_detail(case_id):
    """Detalle de caso - ESENCIAL"""
    try:
        response = requests.get(f"{BACKEND_URL}/cases/{case_id}", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({"error": "Caso no encontrado"}), 404
        else:
            return jsonify({"error": f"Error del backend: {response.status_code}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

@app.route('/api/scan', methods=['POST'])
def trigger_scan():
    """Escaneo manual - ESENCIAL"""
    try:
        response = requests.post(f"{BACKEND_URL}/scan", timeout=30)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error en escaneo: {response.status_code}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')