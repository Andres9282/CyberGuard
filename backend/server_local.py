<<<<<<< HEAD
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json

# Asegurar que el path incluye el directorio backend
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from db_locall import create_tables, create_case, add_event, add_artifact, get_cases, get_case_details


def build_case_report_local(case, events, artifacts):
    """
    Genera un reporte HTML simple basado en los datos del caso (versión local con dicts).
    """
    if not case:
        return """
        <html>
        <head>
            <title>Error - Caso no encontrado</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                .error { color: #b30000; font-size: 24px; }
            </style>
        </head>
        <body>
            <h1 class="error">Caso no encontrado</h1>
            <p>El caso solicitado no existe en la base de datos.</p>
        </body>
        </html>
        """
    
    case_id = case.get("id", "N/A")
    detected_at = case.get("detected_at", "N/A")
    severity = case.get("severity", "N/A")
    process_name = case.get("process_name", "N/A")
    attacker_ip = case.get("attacker_ip", "N/A")
    status = case.get("status", "N/A")
    folder = case.get("folder", "N/A")
    actions = case.get("actions", "[]")
    
    # Parsear actions si es string JSON
    try:
        if isinstance(actions, str):
            actions_list = json.loads(actions)
            actions = ", ".join(actions_list) if isinstance(actions_list, list) else actions
    except:
        pass

    html = f"""
    <html>
    <head>
        <title>Reporte del Caso {case_id}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #b30000;
                border-bottom: 3px solid #b30000;
                padding-bottom: 10px;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                border-left: 4px solid #b30000;
                background: #f5f5f5;
                border-radius: 4px;
            }}
            .section h2 {{
                margin-top: 0;
                color: #333;
            }}
            .info-row {{
                margin: 10px 0;
                padding: 8px 0;
                border-bottom: 1px solid #ddd;
            }}
            .info-row:last-child {{
                border-bottom: none;
            }}
            .label {{
                font-weight: bold;
                color: #555;
                display: inline-block;
                width: 200px;
            }}
            .value {{
                color: #333;
            }}
            ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            li {{
                padding: 10px;
                margin: 5px 0;
                background: white;
                border-radius: 4px;
                border-left: 3px solid #b30000;
            }}
            pre {{
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 4px;
                overflow-x: auto;
            }}
            .severity-high {{
                color: #d32f2f;
                font-weight: bold;
            }}
            .severity-medium {{
                color: #f57c00;
                font-weight: bold;
            }}
            .severity-low {{
                color: #388e3c;
                font-weight: bold;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Reporte del Caso #{case_id}</h1>
            
            <div class="section">
                <h2>Información General</h2>
                <div class="info-row">
                    <span class="label">Fecha de detección:</span>
                    <span class="value">{detected_at}</span>
                </div>
                <div class="info-row">
                    <span class="label">Severidad:</span>
                    <span class="value severity-{severity.lower()}">{severity}</span>
                </div>
                <div class="info-row">
                    <span class="label">Proceso detectado:</span>
                    <span class="value">{process_name}</span>
                </div>
                <div class="info-row">
                    <span class="label">IP atacante:</span>
                    <span class="value">{attacker_ip}</span>
                </div>
                <div class="info-row">
                    <span class="label">Estado:</span>
                    <span class="value">{status}</span>
                </div>
                <div class="info-row">
                    <span class="label">Carpeta afectada:</span>
                    <span class="value">{folder}</span>
                </div>
                <div class="info-row">
                    <span class="label">Acciones tomadas:</span>
                    <span class="value">{actions}</span>
                </div>
            </div>

            <div class="section">
                <h2>Eventos Registrados ({len(events)})</h2>
    """
    
    if events:
        html += "<ul>"
        for e in events:
            timestamp = e.get("timestamp", "N/A")
            event_type = e.get("event_type", "N/A")
            details = e.get("details", "{}")
            
            # Intentar parsear details si es string JSON
            try:
                if isinstance(details, str):
                    details_dict = json.loads(details)
                    details = json.dumps(details_dict, indent=2, ensure_ascii=False)
            except:
                pass
            
            html += f"<li><b>{timestamp}</b> — <strong>{event_type}</strong><br><pre style='margin-top:5px; font-size:12px;'>{details}</pre></li>"
        html += "</ul>"
    else:
        html += "<p>No hay eventos registrados para este caso.</p>"

    html += """
            </div>

            <div class="section">
                <h2>Artefactos Capturados ({})</h2>
    """.format(len(artifacts))
    
    if artifacts:
        html += "<ul>"
        for art in artifacts:
            file_path = art.get("file_path", "N/A")
            file_hash = art.get("hash", "N/A")
            operation = art.get("operation", "N/A")
            html += f"<li><b>Operación:</b> {operation}<br><b>Archivo:</b> {file_path}<br><b>Hash:</b> {file_hash}</li>"
        html += "</ul>"
    else:
        html += "<p>No hay artefactos registrados para este caso.</p>"

    html += """
            </div>
        </div>
    </body>
    </html>
    """

    return html

app = Flask(__name__)
CORS(app)

# Crear tablas al iniciar backend
try:
    create_tables()
    print("✅ Tablas creadas correctamente")
except Exception as e:
    print(f"⚠️ Error al crear tablas: {e}")


@app.route("/event", methods=["POST"])
def receive_event():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # 1. Crear caso
        try:
            case_id = create_case(data)
            print(f"✅ Caso creado con ID: {case_id}")
        except Exception as e:
            print(f"❌ Error al crear caso: {e}")
            return jsonify({"status": "error", "message": f"Error al crear caso: {str(e)}"}), 500

        # 2. Guardar eventos internos
        events_saved = 0
        for ev in data.get("events", []):
            try:
                ev["timestamp"] = ev.get("timestamp") or data.get("timestamp")
                add_event(case_id, ev)
                events_saved += 1
            except Exception as e:
                print(f"⚠️ Error al guardar evento: {e}")

        # 3. Guardar artefactos (evidencias)
        artifacts_saved = 0
        for art in data.get("artifacts", []):
            try:
                add_artifact(case_id, art)
                artifacts_saved += 1
            except Exception as e:
                print(f"⚠️ Error al guardar artefacto: {e}")

        print(f"✅ Caso {case_id}: {events_saved} eventos, {artifacts_saved} artefactos guardados")
        return jsonify({
            "status": "ok", 
            "case_id": case_id,
            "events_saved": events_saved,
            "artifacts_saved": artifacts_saved
        })
    except Exception as e:
        print(f"❌ Error general en /event: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/cases", methods=["GET"])
def list_cases():
    return jsonify(get_cases())


@app.route("/cases/<int:case_id>", methods=["GET"])
def case_details(case_id):
    return jsonify(get_case_details(case_id))


@app.route("/report/<int:case_id>", methods=["GET"])
def report(case_id):
    """Genera y devuelve un reporte HTML del caso especificado"""
    try:
        data = get_case_details(case_id)
        
        # Verificar si el caso existe
        if not data or not data.get("case"):
            return f"""
            <html>
            <head>
                <title>Error - Caso no encontrado</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; }}
                    .container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background: white;
                        padding: 30px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        text-align: center;
                    }}
                    .error {{ color: #b30000; font-size: 28px; margin-bottom: 20px; }}
                    p {{ color: #666; font-size: 16px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="error">⚠️ Caso no encontrado</h1>
                    <p>El caso #{case_id} no existe en la base de datos.</p>
                    <p><a href="/cases" style="color: #b30000;">Ver todos los casos disponibles</a></p>
                </div>
            </body>
            </html>
            """, 404
        
        html = build_case_report_local(
            data["case"],
            data["events"],
            data["artifacts"]
        )
        return html
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"""
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; }}
                .container {{
                    max-width: 800px;
                    margin: 50px auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .error {{ color: #b30000; font-size: 24px; margin-bottom: 20px; }}
                pre {{
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 4px;
                    overflow-x: auto;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="error">❌ Error al generar el reporte</h1>
                <p>Ocurrió un error al intentar generar el reporte del caso {case_id}:</p>
                <pre>{error_details}</pre>
            </div>
        </body>
        </html>
        """, 500


@app.route("/", methods=["GET"])
def home():
    return "CyberGuard Backend OK"


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "backend listo 🔥",
        "message": "Todo funcionando VAMOSSSSSSSSSSS 💪",
        "ok": True
    })


@app.route("/debug/routes", methods=["GET"])
def debug_routes():
    """Endpoint de debug para ver todas las rutas registradas"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "methods": list(rule.methods),
            "rule": rule.rule,
            "endpoint": rule.endpoint
        })
    return jsonify({"routes": routes})


@app.route("/debug/test-data", methods=["POST"])
def create_test_data():
    """Endpoint para crear datos de prueba en la base de datos"""
    from datetime import datetime
    
    test_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "high",
        "folder": "C:\\test\\monitored_folder",
        "actions": ["process_killed", "files_quarantined"],
        "process": {
            "name": "test_process.exe"
        },
        "network": {
            "attacker_ip": "192.168.1.100"
        },
        "events": [
            {
                "event_type": "file_encryption",
                "details": {"files_affected": 10}
            },
            {
                "event_type": "suspicious_activity",
                "details": {"pattern": "ransomware"}
            }
        ],
        "artifacts": [
            {
                "file_path": "C:\\test\\file1.txt",
                "hash": "abc123",
                "operation": "encrypted"
            },
            {
                "file_path": "C:\\test\\file2.txt",
                "hash": "def456",
                "operation": "modified"
            }
        ]
    }
    
    try:
        case_id = create_case(test_data)
        
        for ev in test_data.get("events", []):
            ev["timestamp"] = test_data.get("timestamp")
            add_event(case_id, ev)
        
        for art in test_data.get("artifacts", []):
            add_artifact(case_id, art)
        
        return jsonify({
            "status": "ok",
            "message": f"Datos de prueba creados exitosamente",
            "case_id": case_id
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Debug: mostrar rutas registradas al iniciar
if __name__ == "__main__":
    print("\n📋 Rutas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"   {list(rule.methods)} {rule.rule}")
    print("\n🚀 Iniciando servidor en http://127.0.0.1:5001\n")
    app.run(host="127.0.0.1", port=5001, debug=True)


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

>>>>>>> a9b5778 (Update completo CyberGuard)
