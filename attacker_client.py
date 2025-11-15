# attacker_client.py
# Cliente para ejecutar ataques remotos desde la segunda computadora

import sys
import requests
import argparse
from pathlib import Path

def execute_remote_attack(agent_ip, agent_port, target_folder=None, num_files=10, delay=0.1):
    """
    Ejecuta un ataque remoto en la computadora objetivo.
    
    Args:
        agent_ip: IP de la computadora donde está el agente
        agent_port: Puerto del servidor de ataque remoto
        target_folder: Carpeta objetivo (opcional, usa la del servidor por defecto)
        num_files: Número de archivos a modificar
        delay: Retraso entre modificaciones
    """
    attack_url = f"http://{agent_ip}:{agent_port}/attack"
    
    payload = {
        "num_files": num_files,
        "delay": delay
    }
    
    if target_folder:
        payload["target_folder"] = target_folder
    
    print(f"🔴 Ejecutando ataque remoto...")
    print(f"   Objetivo: {agent_ip}:{agent_port}")
    print(f"   Archivos: {num_files}")
    print(f"   Delay: {delay}s")
    
    try:
        response = requests.post(attack_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ Ataque iniciado exitosamente")
        print(f"   {result.get('message', '')}")
        print(f"   Carpeta objetivo: {result.get('target_folder', 'N/A')}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: No se pudo conectar a {agent_ip}:{agent_port}")
        print(f"   Verifica que el servidor de ataque esté ejecutándose")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Error: Timeout al conectar con {agent_ip}:{agent_port}")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando ataque: {e}")
        return False

def check_agent_status(agent_ip, agent_port):
    """Verifica el estado del servidor de ataque remoto"""
    status_url = f"http://{agent_ip}:{agent_port}/status"
    
    try:
        response = requests.get(status_url, timeout=5)
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Servidor de ataque disponible")
        print(f"   Estado: {result.get('status', 'unknown')}")
        print(f"   Carpeta monitoreada: {result.get('watch_folder', 'N/A')}")
        print(f"   Carpeta existe: {result.get('folder_exists', False)}")
        
        return True
    except Exception as e:
        print(f"❌ Servidor no disponible: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cliente para ejecutar ataques remotos de ransomware simulado"
    )
    parser.add_argument(
        "agent_ip",
        help="IP de la computadora donde está el agente (ej: 192.168.1.100)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=5002,
        help="Puerto del servidor de ataque remoto (default: 5002)"
    )
    parser.add_argument(
        "--folder", "-f",
        help="Carpeta objetivo (opcional, usa la del servidor por defecto)"
    )
    parser.add_argument(
        "--files", "-n",
        type=int,
        default=10,
        help="Número de archivos a modificar (default: 10)"
    )
    parser.add_argument(
        "--delay", "-d",
        type=float,
        default=0.1,
        help="Retraso entre modificaciones en segundos (default: 0.1)"
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Solo verificar el estado del servidor"
    )
    
    args = parser.parse_args()
    
    if args.status:
        check_agent_status(args.agent_ip, args.port)
    else:
        execute_remote_attack(
            args.agent_ip,
            args.port,
            args.folder,
            args.files,
            args.delay
        )

