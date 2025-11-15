# backend/config.py
# Configuración centralizada para conexiones entre computadoras

import os
from pathlib import Path

# Configuración del Backend (Computadora 1 - Servidor)
BACKEND_HOST = os.getenv("CYBERGUARD_BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("CYBERGUARD_BACKEND_PORT", "5001"))

# URL del backend para que el agente se conecte
# Por defecto usa localhost, pero debe configurarse con la IP real de la computadora servidor
# Se puede sobrescribir con variable de entorno CYBERGUARD_BACKEND_URL
# IMPORTANTE: Debe incluir el endpoint /event para que el agente pueda enviar eventos
BACKEND_URL = os.getenv(
    "CYBERGUARD_BACKEND_URL", 
    f"http://10.74.10.88:5001"  #IP del puerto
)

# Configuración del Agente (Computadora 2 - Cliente)
AGENT_HOST = os.getenv("CYBERGUARD_AGENT_HOST", "0.0.0.0")
AGENT_PORT = int(os.getenv("CYBERGUARD_AGENT_PORT", "5002"))

# Carpeta a monitorear (puede ser diferente en cada computadora)
# Windows usa C:\attack_test, Linux/WSL usa /home/andres/attack_test
if os.name == 'nt':  # Windows
    DEFAULT_FOLDER = "C:\\attack_test"
else:  # Linux/WSL
    DEFAULT_FOLDER = "/home/andres/attack_test"

FOLDER_TO_WATCH = os.getenv("CYBERGUARD_WATCH_FOLDER", DEFAULT_FOLDER)

# Configuración de red para ataque remoto
# IP de la computadora donde está el agente (para ataques remotos)
AGENT_IP = os.getenv("CYBERGUARD_AGENT_IP", "10.74.10.88")
AGENT_ATTACK_URL = f"http://{AGENT_IP}:{AGENT_PORT}/attack"

# Cooldown para detección de eventos
COOLDOWN_SECONDS = int(os.getenv("CYBERGUARD_COOLDOWN", "5"))

