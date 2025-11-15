# app_integrated_real.py - VERSIÓN SIN DATOS MOCK
from flask import Flask, render_template, jsonify, request
import sqlite3
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Configuración de base de datos REAL
DB_PATH = Path("database/cyberguard.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Tablas REALES (igual que tu backend)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detected_at TEXT,
            severity TEXT,
            process_name TEXT,
            attacker_ip TEXT,
            folder TEXT,
            actions TEXT,
            status TEXT DEFAULT 'detenido'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            timestamp TEXT,
            event_type TEXT,
            details TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            file_path TEXT,
            hash TEXT,
            operation TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )
    """)

    conn.commit()
    conn.close()

create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Estado REAL del sistema - basado en datos reales de la BD"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Contar casos REALES de la base de datos
        cur.execute("SELECT COUNT(*) as count FROM cases WHERE severity IN ('critical', 'high')")
        critical_cases = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as total FROM cases")
        total_cases = cur.fetchone()['total']
        
        conn.close()

        if critical_cases > 0:
            status_info = {
                "status": "ATAQUE",
                "message": f"{critical_cases} incidente(s) crítico(s) activo(s)",
                "total_cases": total_cases,
                "last_update": datetime.now().isoformat()
            }
        elif total_cases > 0:
            status_info = {
                "status": "ESCUDO", 
                "message": f"Sistema protegido - {total_cases} caso(s) históricos",
                "total_cases": total_cases,
                "last_update": datetime.now().isoformat()
            }
        else:
            status_info = {
                "status": "NORMAL",
                "message": "Sistema funcionando correctamente - Sin incidentes",
                "total_cases": 0,
                "last_update": datetime.now().isoformat()
            }
        
        return jsonify(status_info)
        
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": f"Error verificando estado: {str(e)}",
            "last_update": datetime.now().isoformat()
        })

@app.route('/api/cases')
def get_cases():
    """Casos REALES de la base de datos"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                id,
                detected_at as fecha,
                severity as gravedad,
                process_name as proceso,
                attacker_ip as ip,
                folder as tipo_ataque,
                status,
                actions
            FROM cases 
            ORDER BY id DESC
        """)
        rows = cur.fetchall()
        conn.close()

        cases = []
        for row in rows:
            case = dict(row)
            # Convertir gravedad al formato del frontend
            severity_map = {
                'critical': 'crítico', 'high': 'alto', 
                'medium': 'medio', 'low': 'bajo'
            }
            case['gravedad'] = severity_map.get(case['gravedad'], case['gravedad'])
            cases.append(case)

        return jsonify(cases)
        
    except Exception as e:
        print(f"Error getting cases: {e}")
        return jsonify({"error": str(e), "cases": []})

@app.route('/api/cases/<int:case_id>')
def get_case_detail(case_id):
    """Detalle REAL del caso"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Datos básicos del caso
        cur.execute("""
            SELECT 
                id,
                detected_at as fecha,
                severity as gravedad,
                process_name as proceso,
                attacker_ip as ip,
                folder as tipo_ataque,
                actions
            FROM cases WHERE id = ?
        """, (case_id,))
        
        case_row = cur.fetchone()
        if not case_row:
            return jsonify({"error": "Caso no encontrado"}), 404
        
        case_data = dict(case_row)
        
        # Obtener eventos REALES del caso
        cur.execute("""
            SELECT timestamp, event_type, details 
            FROM events WHERE case_id = ?
        """, (case_id,))
        events = [dict(row) for row in cur.fetchall()]
        
        # Obtener artefactos REALES
        cur.execute("""
            SELECT file_path, hash, operation 
            FROM artifacts WHERE case_id = ?
        """, (case_id,))
        artifacts = [dict(row) for row in cur.fetchall()]
        
        conn.close()

        # Procesar acciones REALES
        actions = []
        try:
            actions = json.loads(case_data.get('actions', '[]'))
        except:
            actions = []
        
        # Estructurar datos REALES para el frontend
        enhanced_case = {
            "id": case_data["id"],
            "fecha": case_data["fecha"],
            "gravedad": case_data["gravedad"],
            "proceso": case_data["proceso"],
            "ip": case_data["ip"],
            "tipo_ataque": case_data["tipo_ataque"],
            "archivos_afectados": [
                {
                    "ruta": art["file_path"],
                    "hash": art["hash"]
                } for art in artifacts
            ],
            "proceso_terminado": "process_terminated" in actions,
            "ip_bloqueada": "ip_blocked" in actions,
            "usuario_deshabilitado": "user_disabled" in actions
        }
        
        return jsonify(enhanced_case)
        
    except Exception as e:
        print(f"Error getting case detail: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan', methods=['POST'])
def trigger_scan():
    """ESCANEO REAL - No crea datos falsos"""
    try:
        # En lugar de crear datos mock, aquí deberías llamar a tu escáner real
        # Por ahora solo actualiza el estado
        return jsonify({
            "status": "success", 
            "message": "Escaneo iniciado - Revisa los agentes de seguridad",
            "note": "Los casos aparecerán cuando se detecten amenazas reales"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para recibir eventos REALES de agentes
@app.route("/event", methods=["POST"])
def receive_event():
    """Recibir eventos REALES de agentes de seguridad"""
    try:
        data = request.json
        conn = get_connection()
        cur = conn.cursor()

        # Procesar datos REALES del agente
        timestamp = data.get("timestamp", datetime.now().isoformat())
        severity = data.get("severity", "medium")
        process_name = data.get("process_name", "unknown")
        attacker_ip = data.get("attacker_ip", "unknown")
        
        # Insertar caso REAL
        cur.execute("""
            INSERT INTO cases (detected_at, severity, process_name, attacker_ip, folder, actions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            severity,
            process_name,
            attacker_ip,
            data.get("attack_type", "unknown"),
            json.dumps(data.get("actions", []))
        ))
        
        case_id = cur.lastrowid
        
        # Insertar eventos REALES si existen
        if "events" in data:
            for event in data["events"]:
                cur.execute("""
                    INSERT INTO events (case_id, timestamp, event_type, details)
                    VALUES (?, ?, ?, ?)
                """, (
                    case_id,
                    event.get("timestamp", timestamp),
                    event.get("event_type", "security_event"),
                    json.dumps(event.get("details", {}))
                ))
        
        # Insertar artefactos REALES si existen
        if "artifacts" in data:
            for artifact in data["artifacts"]:
                cur.execute("""
                    INSERT INTO artifacts (case_id, file_path, hash, operation)
                    VALUES (?, ?, ?, ?)
                """, (
                    case_id,
                    artifact.get("file_path", ""),
                    artifact.get("hash", ""),
                    artifact.get("operation", "detected")
                ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "ok", 
            "case_id": case_id,
            "message": "Evento de seguridad registrado correctamente"
        })
        
    except Exception as e:
        print(f"Error receiving event: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 CyberGuard SV - Sistema REAL")
    print("📊 Dashboard: http://localhost:5000")
    print("💾 Base de datos: database/cyberguard.db")
    print("📝 Nota: Los casos mostrados son REALES de la base de datos")
    app.run(debug=True, port=5000, host='0.0.0.0')