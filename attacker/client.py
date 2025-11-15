# attacker/client.py
import requests
import json

SERVER_IP = "100.82.42.122"   # IP Tailscale del backend
BACKEND_PORT = 5001

url = f"http://{SERVER_IP}:{BACKEND_PORT}/event"

payload = {
    "features": {
        "size_change": 999,
        "created": 40,
        "deleted": 20,
        "encrypted": 15,
        "rapid_changes": 100
    }
}

print("📤 Enviando ataque…")
resp = requests.post(url, json=payload)
print("📥 Respuesta del servidor:", resp.json())
