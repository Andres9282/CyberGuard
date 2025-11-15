# backend/reports/report_builder.py

from datetime import datetime

def build_case_report(case, events, evidence):
    """
    Construye un reporte HTML simple para visualizar los detalles del caso.
    case: dict con info del caso
    events: lista de dicts con eventos
    evidence: lista o dict con evidencia capturada
    """

    html = """
    <html>
    <head>
        <title>Reporte de Caso CyberGuard</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f4; }
            h1 { color: #003366; }
            h2 { color: #004c99; }
            .box { background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            table, th, td { border: 1px solid #ccc; }
            th, td { padding: 8px; text-align: left; }
            th { background: #e6f0ff; }
        </style>
    </head>
    <body>
    """

    # -------------------------
    # HEADER
    # -------------------------
    html += "<h1>Reporte de Caso CyberGuard</h1>"
    html += f"<p>Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"

    # -------------------------
    # INFO DEL CASO
    # -------------------------

    html += '<div class="box">'
    html += "<h2>Información del Caso</h2>"
    html += "<table>"

    for key, value in case.items():
        html += f"<tr><th>{key}</th><td>{value}</td></tr>"

    html += "</table></div>"

    # -------------------------
    # EVENTOS DEL CASO
    # -------------------------

    html += '<div class="box">'
    html += "<h2>Eventos Registrados</h2>"

    if events:
        html += "<table><tr><th>Timestamp</th><th>Tipo</th><th>Detalles</th></tr>"
        for ev in events:
            html += f"""
            <tr>
                <td>{ev.get('timestamp','')}</td>
                <td>{ev.get('type','')}</td>
                <td>{ev.get('details','')}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += "<p>No hay eventos registrados.</p>"

    html += "</div>"

    # -------------------------
    # EVIDENCIA
    # -------------------------

    html += '<div class="box">'
    html += "<h2>Evidencia Capturada</h2>"

    html += "<pre>" + str(evidence) + "</pre>"

    html += "</div>"

    # CERRAR HTML
    html += "</body></html>"

    return html
