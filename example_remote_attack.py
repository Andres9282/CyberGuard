# example_remote_attack.py
# Ejemplo de cómo ejecutar un ataque remoto desde Python

import requests
import json

# Configuración
AGENT_IP = "192.168.1.100"  # Cambiar por la IP de la computadora 2
AGENT_PORT = 5002
BACKEND_IP = "192.168.1.50"  # Cambiar por la IP de la computadora 1
BACKEND_PORT = 5001

def example_direct_attack():
    """Ejemplo: Ataque directo a la computadora 2"""
    print("🔴 Ejemplo 1: Ataque directo a computadora 2")
    
    attack_url = f"http://{AGENT_IP}:{AGENT_PORT}/attack"
    payload = {
        "num_files": 10,
        "delay": 0.1
    }
    
    try:
        response = requests.post(attack_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Ataque iniciado: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_via_backend():
    """Ejemplo: Ataque a través del backend (computadora 1)"""
    print("\n🔴 Ejemplo 2: Ataque a través del backend")
    
    backend_url = f"http://{BACKEND_IP}:{BACKEND_PORT}/trigger-attack"
    payload = {
        "agent_ip": AGENT_IP,
        "agent_port": AGENT_PORT,
        "num_files": 15,
        "delay": 0.05
    }
    
    try:
        response = requests.post(backend_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Ataque iniciado: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_status():
    """Verificar estado de los servidores"""
    print("\n📊 Verificando estado de servidores...")
    
    # Verificar servidor de ataque
    try:
        response = requests.get(f"http://{AGENT_IP}:{AGENT_PORT}/status", timeout=5)
        print(f"✅ Servidor de ataque: {response.json()}")
    except Exception as e:
        print(f"❌ Servidor de ataque no disponible: {e}")
    
    # Verificar backend
    try:
        response = requests.get(f"http://{BACKEND_IP}:{BACKEND_PORT}/", timeout=5)
        print(f"✅ Backend: {response.text}")
    except Exception as e:
        print(f"❌ Backend no disponible: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Ejemplos de Ataque Remoto - CyberGuard")
    print("=" * 60)
    print(f"\nConfiguración:")
    print(f"  Computadora 2 (Agente): {AGENT_IP}:{AGENT_PORT}")
    print(f"  Computadora 1 (Backend): {BACKEND_IP}:{BACKEND_PORT}")
    print("\n⚠️  IMPORTANTE: Actualiza las IPs en este script antes de ejecutar")
    print("=" * 60)
    
    # Verificar estado primero
    check_status()
    
    # Ejecutar ejemplos
    # Descomenta las líneas siguientes para ejecutar ataques:
    # example_direct_attack()
    # example_via_backend()

