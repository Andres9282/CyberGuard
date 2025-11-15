# backend/db.py
import sqlite3
import json
from pathlib import Path

# Usar ruta absoluta basada en la ubicación del archivo para evitar problemas
# cuando se ejecuta desde diferentes directorios
DB_PATH = Path(__file__).resolve().parents[1] / "database" / "cyberguard.db"



def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    conn = get_connection()
    c = conn.cursor()

    # Tabla de casos
    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detected_at TEXT,
            severity TEXT,
            process_name TEXT,
            attacker_ip TEXT,
            folder TEXT,
            actions TEXT
        )
    """)

    # Tabla de eventos
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            timestamp TEXT,
            event_type TEXT,
            details TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )
    """)

    # Tabla de evidencia
    c.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            evidence_json TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )
    """)

    conn.commit()
    conn.close()


def create_case(data):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO cases (detected_at, severity, process_name, attacker_ip, folder, actions)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["severity"],
        data["process_name"],
        data.get("attacker_ip", "unknown"),
        data["folder"],
        json.dumps(data["actions"])
    ))

    case_id = c.lastrowid
    conn.commit()
    conn.close()
    return case_id


def add_event(case_id, event):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO events (case_id, timestamp, event_type, details)
        VALUES (?, ?, ?, ?)
    """, (
        case_id,
        event["timestamp"],
        event["type"],
        json.dumps(event.get("details", {}))
    ))

    conn.commit()
    conn.close()


def add_evidence(case_id, evidence_json):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO evidence (case_id, evidence_json)
        VALUES (?, ?)
    """, (case_id, json.dumps(evidence_json)))

    conn.commit()
    conn.close()


def get_cases():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM cases ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()
    return rows


def get_case_details(case_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM cases WHERE id=?", (case_id,))
    case = c.fetchone()

    c.execute("SELECT * FROM events WHERE case_id=?", (case_id,))
    events = c.fetchall()

    c.execute("SELECT evidence_json FROM evidence WHERE case_id=?", (case_id,))
    evidence = [json.loads(e[0]) for e in c.fetchall()]

    conn.close()

    return {
        "case": case,
        "events": events,
        "evidence": evidence
    }
