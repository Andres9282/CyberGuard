# backend/schema.py

CREATE_CASES_TABLE = """
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    detected_at TEXT NOT NULL,
    severity TEXT NOT NULL,
    process_name TEXT,
    attacker_ip TEXT,
    status TEXT DEFAULT 'detenido'
);
"""

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    details TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(id)
);
"""

CREATE_ARTIFACTS_TABLE = """
CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    file_path TEXT,
    file_hash TEXT,
    operation TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(id)
);
"""
