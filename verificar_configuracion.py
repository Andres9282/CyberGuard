# verificar_configuracion.py
# Script para verificar que la configuración está correcta antes de ejecutar

import os
import sys
import socket
import requests
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_file_exists(filepath, description):
    """Verifica que un archivo exista"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: NO ENCONTRADO - {filepath}")
        return False

def check_config():
    """Verifica la configuración"""
    print_header("VERIFICANDO CONFIGURACIÓN")
    
    config_path = Path("backend/config.py")
    if not config_path.exists():
        print("❌ backend/config.py no existe")
        return False
    
    print("✅ backend/config.py existe")
    
    # Intentar importar configuración
    try:
        sys.path.insert(0, str(Path.cwd()))
        from backend.config import (
            BACKEND_HOST, BACKEND_PORT, AGENT_HOST, AGENT_PORT,
            FOLDER_TO_WATCH, BACKEND_URL, AGENT_IP
        )
        
        print(f"\n📋 Configuración actual:")
        print(f"   Backend Host: {BACKEND_HOST}")
        print(f"   Backend Port: {BACKEND_PORT}")
        print(f"   Backend URL: {BACKEND_URL}")
        print(f"   Agent Host: {AGENT_HOST}")
        print(f"   Agent Port: {AGENT_PORT}")
        print(f"   Agent IP: {AGENT_IP}")
        print(f"   Carpeta monitoreada: {FOLDER_TO_WATCH}")
        
        # Verificar carpeta
        if Path(FOLDER_TO_WATCH).exists():
            print(f"✅ Carpeta existe: {FOLDER_TO_WATCH}")
            files = list(Path(FOLDER_TO_WATCH).glob("*"))
            print(f"   Archivos encontrados: {len([f for f in files if f.is_file()])}")
        else:
            print(f"⚠️  Carpeta NO existe: {FOLDER_TO_WATCH}")
            print(f"   Ejecuta: mkdir -p {FOLDER_TO_WATCH}")
        
        return True
    except ImportError as e:
        print(f"❌ Error importando configuración: {e}")
        return False

def check_ports():
    """Verifica que los puertos estén disponibles"""
    print_header("VERIFICANDO PUERTOS")
    
    try:
        from backend.config import BACKEND_PORT, AGENT_PORT
        
        # Verificar puerto backend
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', BACKEND_PORT))
        sock.close()
        
        if result == 0:
            print(f"✅ Puerto {BACKEND_PORT} (Backend) está en uso (servidor corriendo)")
        else:
            print(f"⚠️  Puerto {BACKEND_PORT} (Backend) está libre (servidor no corriendo)")
        
        # Verificar puerto agente
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', AGENT_PORT))
        sock.close()
        
        if result == 0:
            print(f"✅ Puerto {AGENT_PORT} (Agente) está en uso (servidor corriendo)")
        else:
            print(f"⚠️  Puerto {AGENT_PORT} (Agente) está libre (servidor no corriendo)")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando puertos: {e}")
        return False

def check_services():
    """Verifica que los servicios estén corriendo"""
    print_header("VERIFICANDO SERVICIOS")
    
    try:
        from backend.config import BACKEND_PORT, AGENT_PORT, AGENT_IP
        
        # Verificar backend
        try:
            response = requests.get(f"http://localhost:{BACKEND_PORT}/", timeout=2)
            if response.status_code == 200:
                print(f"✅ Backend respondiendo en puerto {BACKEND_PORT}")
            else:
                print(f"⚠️  Backend responde pero con código {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Backend NO está corriendo en puerto {BACKEND_PORT}")
        except Exception as e:
            print(f"⚠️  Error verificando backend: {e}")
        
        # Verificar servidor de ataque
        try:
            response = requests.get(f"http://localhost:{AGENT_PORT}/status", timeout=2)
            if response.status_code == 200:
                print(f"✅ Servidor de ataque respondiendo en puerto {AGENT_PORT}")
                data = response.json()
                print(f"   Estado: {data.get('status', 'unknown')}")
            else:
                print(f"⚠️  Servidor de ataque responde pero con código {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Servidor de ataque NO está corriendo en puerto {AGENT_PORT}")
        except Exception as e:
            print(f"⚠️  Error verificando servidor de ataque: {e}")
        
        # Verificar servidor de ataque remoto (si AGENT_IP no es localhost)
        if AGENT_IP and AGENT_IP != "localhost":
            try:
                response = requests.get(f"http://{AGENT_IP}:{AGENT_PORT}/status", timeout=2)
                if response.status_code == 200:
                    print(f"✅ Servidor de ataque remoto accesible en {AGENT_IP}:{AGENT_PORT}")
                else:
                    print(f"⚠️  Servidor remoto responde pero con código {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"❌ No se puede conectar al servidor remoto {AGENT_IP}:{AGENT_PORT}")
                print(f"   Verifica que el servidor esté corriendo y la IP sea correcta")
            except Exception as e:
                print(f"⚠️  Error verificando servidor remoto: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando servicios: {e}")
        return False

def check_files():
    """Verifica que los archivos necesarios existan"""
    print_header("VERIFICANDO ARCHIVOS")
    
    files_to_check = [
        ("backend/server.py", "Servidor backend"),
        ("backend/config.py", "Configuración"),
        ("backend/db.py", "Base de datos"),
        ("agent/monitor.py", "Monitor de agente"),
        ("agent/remote_attack_server.py", "Servidor de ataque remoto"),
        ("agent/ransomware_test.py", "Simulador de ataque"),
        ("attacker_client.py", "Cliente de ataque"),
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def get_local_ip():
    """Obtiene la IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "No disponible"

def main():
    print_header("VERIFICACIÓN DE CONFIGURACIÓN - CyberGuard")
    
    local_ip = get_local_ip()
    print(f"\n📍 Tu IP local: {local_ip}")
    print(f"   (Úsala para configurar BACKEND_URL en la otra computadora)")
    
    # Verificar archivos
    files_ok = check_files()
    
    # Verificar configuración
    config_ok = check_config()
    
    # Verificar puertos
    ports_ok = check_ports()
    
    # Verificar servicios
    services_ok = check_services()
    
    # Resumen
    print_header("RESUMEN")
    
    if files_ok and config_ok:
        print("✅ Archivos y configuración: OK")
    else:
        print("❌ Archivos y configuración: REVISAR")
    
    if ports_ok:
        print("✅ Puertos: OK")
    else:
        print("⚠️  Puertos: REVISAR")
    
    if services_ok:
        print("✅ Servicios: OK (o no están corriendo, lo cual es normal)")
    else:
        print("⚠️  Servicios: REVISAR")
    
    print("\n" + "=" * 60)
    print("📚 Para más información, ver: TUTORIAL_ATAQUE_REMOTO.md")
    print("=" * 60)

if __name__ == "__main__":
    main()

