import sqlite3
import json
from datetime import datetime

DB_PATH = r"C:\CyberGuardData\database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detected_at TEXT,
            severity TEXT,
            process_name TEXT,
            attacker_ip TEXT,
            status TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            timestamp TEXT,
            event_type TEXT,
            details TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            file_path TEXT,
            hash TEXT,
            operation TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        );
    """)

    conn.commit()
    conn.close()


def create_case(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cases(detected_at, severity, process_name, attacker_ip, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("timestamp"),
        data.get("severity"),
        data["process"]["name"],
        data["network"]["attacker_ip"],
        "detenido"
    ))

    conn.commit()
    case_id = cur.lastrowid
    conn.close()
    return case_id


def add_event(case_id, event):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO events(case_id, timestamp, event_type, details)
        VALUES (?, ?, ?, ?)
    """, (
        case_id,
        event.get("timestamp", datetime.utcnow().isoformat()),
        event["event_type"],
        json.dumps(event.get("details", {}))
    ))

    conn.commit()
    conn.close()


def add_artifact(case_id, artifact):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO artifacts(case_id, file_path, hash, operation)
        VALUES (?, ?, ?, ?)
    """, (
        case_id,
        artifact["file_path"],
        artifact["hash"],
        artifact["operation"]
    ))

    conn.commit()
    conn.close()


def get_cases():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cases ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_case_details(case_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = cur.fetchone()

    cur.execute("SELECT * FROM events WHERE case_id = ?", (case_id,))
    events = cur.fetchall()

    cur.execute("SELECT * FROM artifacts WHERE case_id = ?", (case_id,))
    artifacts = cur.fetchall()

    conn.close()

    return {
        "case": dict(case) if case else None,
        "events": [dict(e) for e in events],
        "artifacts": [dict(a) for a in artifacts]
    }
