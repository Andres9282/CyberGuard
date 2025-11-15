# backend/config.py
# Configuración centralizada para conexiones entre computadoras

import os
from pathlib import Path

# ---------------------------------------------------------
# BACKEND (PC1 – VÍCTIMA)
# ---------------------------------------------------------
BACKEND_HOST = os.getenv("CYBERGUARD_BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("CYBERGUARD_BACKEND_PORT", "5001"))

# URL donde el agente le enviará eventos
BACKEND_URL = os.getenv(
    "CYBERGUARD_BACKEND_URL",
    "http://10.74.10.88:5001/event"   # 👈 IP del backend (PC1)
)

# ---------------------------------------------------------
# AGENTE (PC1 – MONITOR)
# ---------------------------------------------------------
AGENT_HOST = os.getenv("CYBERGUARD_AGENT_HOST", "0.0.0.0")
AGENT_PORT = int(os.getenv("CYBERGUARD_AGENT_PORT", "5002"))

# Carpeta a monitorear
if os.name == "nt":
    DEFAULT_FOLDER = "C:\\attack_test"
else:
    DEFAULT_FOLDER = "/home/andres/attack_test"

FOLDER_TO_WATCH = os.getenv("CYBERGUARD_WATCH_FOLDER", DEFAULT_FOLDER)

# ---------------------------------------------------------
# ATAQUES REMOTOS (desde PC2)
# ---------------------------------------------------------
# IP del agente (PC1)
AGENT_IP = os.getenv("CYBERGUARD_AGENT_IP", "10.74.10.88")  

AGENT_ATTACK_URL = f"http://{AGENT_IP}:{AGENT_PORT}/attack"

# ---------------------------------------------------------
# OTROS PARÁMETROS
# ---------------------------------------------------------
COOLDOWN_SECONDS = int(os.getenv("CYBERGUARD_COOLDOWN", "5"))
