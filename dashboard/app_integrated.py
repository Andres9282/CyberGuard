# app_integrated.py - CyberGuard Backend + Frontend Integrado
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde cualquier origen

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
            features TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )
    """)
    
    # Agregar columna features si no existe (para bases de datos existentes)
    try:
        cur.execute("ALTER TABLE events ADD COLUMN features TEXT")
    except sqlite3.OperationalError:
        pass  # La columna ya existe

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
    """Página principal del dashboard"""
    try:
        return render_template('index.html')
    except Exception as e:
        import traceback
        error_msg = f"Error cargando template: {str(e)}\n\n{traceback.format_exc()}"
        return error_msg, 500

@app.route('/api/test')
def test_connection():
    """Endpoint de prueba para verificar que el servidor funciona"""
    return jsonify({
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def get_status():
    """Estado REAL del sistema - basado en datos reales de la BD"""
    try:
        print(f"[API] GET /api/status - {datetime.now().strftime('%H:%M:%S')}")
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
        
        print(f"[API] Status response: {status_info['status']} - {total_cases} casos")
        
        # Agregar información adicional para alertas automáticas
        status_info['has_attack'] = critical_cases > 0
        status_info['critical_count'] = critical_cases
        
        return jsonify(status_info)
        
    except Exception as e:
        print(f"[API] ERROR en /api/status: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "ERROR",
            "message": f"Error verificando estado: {str(e)}",
            "last_update": datetime.now().isoformat()
        })

@app.route('/api/cases')
def get_cases():
    """Casos REALES de la base de datos"""
    try:
        print(f"[API] GET /api/cases - {datetime.now().strftime('%H:%M:%S')}")
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

        print(f"[API] Casos encontrados: {len(cases)}")
        return jsonify(cases)
        
    except Exception as e:
        print(f"[API] ERROR en /api/cases: {e}")
        import traceback
        traceback.print_exc()
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
    """ESCANEO REAL - Revisa la base de datos para detectar ataques"""
    try:
        print(f"[SCAN] Escaneo iniciado - {datetime.now().strftime('%H:%M:%S')}")
        conn = get_connection()
        cur = conn.cursor()
        
        # Buscar casos críticos o de alta severidad
        cur.execute("""
            SELECT 
                id,
                detected_at,
                severity,
                process_name,
                attacker_ip,
                folder as attack_type
            FROM cases 
            WHERE severity IN ('critical', 'high')
            ORDER BY detected_at DESC
            LIMIT 10
        """)
        critical_cases = cur.fetchall()
        
        # Contar todos los casos
        cur.execute("SELECT COUNT(*) as total FROM cases")
        total_cases = cur.fetchone()['total']
        
        # Contar casos críticos
        cur.execute("SELECT COUNT(*) as count FROM cases WHERE severity IN ('critical', 'high')")
        critical_count = cur.fetchone()['count']
        
        conn.close()
        
        # Preparar respuesta
        scan_result = {
            "status": "success",
            "has_attack": critical_count > 0,
            "total_cases": total_cases,
            "critical_cases": critical_count,
            "cases": []
        }
        
        # Agregar detalles de casos críticos
        for case in critical_cases:
            case_dict = dict(case)
            scan_result["cases"].append({
                "id": case_dict["id"],
                "detected_at": case_dict["detected_at"],
                "severity": case_dict["severity"],
                "process_name": case_dict["process_name"],
                "attacker_ip": case_dict["attacker_ip"],
                "attack_type": case_dict["attack_type"]
            })
        
        if critical_count > 0:
            scan_result["message"] = f"🚨 ALERTA: Se detectaron {critical_count} ataque(s) crítico(s)"
            scan_result["alert_type"] = "danger"
        else:
            scan_result["message"] = "✅ Sistema seguro - No se detectaron ataques"
            scan_result["alert_type"] = "success"
        
        print(f"[SCAN] Resultado: {critical_count} casos críticos de {total_cases} totales")
        return jsonify(scan_result)
        
    except Exception as e:
        print(f"[SCAN] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "has_attack": False,
            "message": f"Error durante el escaneo: {str(e)}",
            "alert_type": "error"
        }), 500

# Endpoint para recibir eventos REALES de agentes
@app.route("/event", methods=["POST"])
def receive_event():
    """Recibir eventos REALES de agentes de seguridad"""
    try:
        print(f"\n{'='*60}")
        print(f"[EVENT] POST /event recibido - {datetime.now().strftime('%H:%M:%S')}")
        data = request.json
        if not data:
            print("[EVENT] ERROR: No se recibieron datos JSON")
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400
        
        print(f"[EVENT] Datos recibidos:")
        print(f"   - Severity: {data.get('severity', 'N/A')}")
        print(f"   - Process: {data.get('process_name', 'N/A')}")
        print(f"   - IP: {data.get('attacker_ip', 'N/A')}")
        print(f"   - Attack Type: {data.get('attack_type', 'N/A')}")
        
        conn = get_connection()
        cur = conn.cursor()

        # ============================
        # Extraer data del agente
        # ============================

        timestamp = data.get("timestamp", datetime.now().isoformat())
        severity = data.get("severity", "medium")
        process_name = data.get("process_name", "unknown")
        attacker_ip = data.get("attacker_ip", "unknown")

        # ⚠️ features que vienen del agente
        features = data.get("features", {})

        # ============================
        # Insertar caso REAL
        # ============================

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

        # ============================
        # Insertar eventos REALES
        # incluyendo FEATURES AQUÍ
        # ============================

        if "events" in data:
            for event in data["events"]:
                cur.execute("""
                    INSERT INTO events (case_id, timestamp, event_type, details, features)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    case_id,
                    event.get("timestamp", timestamp),
                    event.get("event_type", "security_event"),
                    json.dumps(event.get("details", {})),
                    json.dumps(features)   # <-- GUARDAR FEATURES AQUI
                ))

        # ============================
        # Insertar artefactos REALES
        # ============================

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

        print(f"[EVENT] ✅ Evento guardado exitosamente")
        print(f"   - Case ID: {case_id}")
        print(f"   - Eventos guardados: {len(data.get('events', []))}")
        print(f"   - Artefactos guardados: {len(data.get('artifacts', []))}")
        print(f"{'='*60}\n")
        
        return jsonify({
            "status": "ok",
            "case_id": case_id,
            "message": "Evento de seguridad registrado correctamente"
        })

    except Exception as e:
        print(f"❌ Error receiving event: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/report/<int:case_id>/pdf')
def download_pdf_report(case_id):
    """Generar y descargar reporte en PDF"""
    try:
        # Obtener datos del caso
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, detected_at, severity, process_name, attacker_ip, folder, actions
            FROM cases WHERE id = ?
        """, (case_id,))
        
        case = cur.fetchone()
        if not case:
            return jsonify({"error": "Caso no encontrado"}), 404
        
        case_dict = dict(case)
        conn.close()

        # Crear PDF en memoria
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Contenido del PDF
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=20,
            alignment=1,
            textColor=colors.black
        )
        story.append(Paragraph("INFORME FORENSE - CYBERGUARD SV", title_style))
        story.append(Spacer(1, 15))
        
        # Información del caso
        story.append(Paragraph("<b>INFORMACIÓN DEL CASO</b>", styles['Heading2']))
        
        case_data = [
            ["Número de Caso:", f"#{case_dict['id']}"],
            ["Fecha de Detección:", case_dict['detected_at']],
            ["Gravedad:", case_dict['severity'].upper()],
            ["Proceso:", case_dict['process_name']],
            ["IP Atacante:", case_dict['attacker_ip']],
            ["Tipo de Ataque:", case_dict['folder']],
        ]
        
        case_table = Table(case_data, colWidths=[2*inch, 3*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ]))
        
        story.append(case_table)
        story.append(Spacer(1, 15))
        
        # Acciones tomadas
        story.append(Paragraph("<b>ACCIONES DE MITIGACIÓN</b>", styles['Heading2']))
        try:
            actions = json.loads(case_dict.get('actions', '[]'))
            actions_text = ", ".join(actions) if actions else "Ninguna acción registrada"
        except:
            actions_text = "Ninguna acción registrada"
            
        story.append(Paragraph(actions_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Pie de página
        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"<i>Reporte generado: {generated_time}</i>", styles['Italic']))
        story.append(Paragraph("<i>CyberGuard SV - Sistema de detección de ransomware</i>", styles['Italic']))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"reporte_caso_{case_id}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import socket
    
    print("=" * 70)
    print("🚀 CYBERGUARD SV - SERVIDOR INICIADO")
    print("=" * 70)
    print("🌐 URLs de acceso:")
    print(f"   • Local: http://localhost:5000")
    print(f"   • Red REAL: http://10.74.11.116:5000  ← ✅ USA ESTA CON LOS DEMÁS")
    print(f"   • Otra red: http://192.168.137.1:5000  ← ❌ NO usar esta")
    print("")
    print("📋 Instrucciones para tu equipo:")
    print("   1. Todos deben estar en la MISMA red WiFi/Ethernet")
    print("   2. Usar: http://10.74.11.116:5000")
    print("   3. Si no funciona, verificar firewall")
    print("=" * 70)
    
    # Ejecutar servidor
    app.run(debug=True, port=5000, host='0.0.0.0', threaded=True)