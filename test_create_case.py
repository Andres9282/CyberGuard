#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear un caso de prueba en el backend
"""
import requests
import json
import sys
from datetime import datetime

# Configurar stdout para UTF-8 en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# URL del backend
BACKEND_URL = "http://127.0.0.1:5001"

def create_test_case():
    """Crea un caso de prueba usando el endpoint /debug/test-data"""
    print("🔄 Creando caso de prueba...")
    
    try:
        response = requests.post(f"{BACKEND_URL}/debug/test-data")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Caso creado exitosamente!")
            print(f"   Case ID: {data.get('case_id')}")
            print(f"   Mensaje: {data.get('message')}")
            return data.get('case_id')
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5001")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def create_custom_case():
    """Crea un caso personalizado usando el endpoint /event"""
    print("\n🔄 Creando caso personalizado...")
    
    case_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "high",
        "folder": "C:\\Users\\Test\\Documents\\Sensitive",
        "actions": ["process_killed", "files_quarantined", "network_blocked"],
        "process": {
            "name": "suspicious_malware.exe"
        },
        "network": {
            "attacker_ip": "192.168.1.50"
        },
        "events": [
            {
                "event_type": "file_encryption_detected",
                "details": {
                    "files_affected": 25,
                    "encryption_pattern": "AES-256",
                    "ransom_note_found": True
                }
            },
            {
                "event_type": "network_anomaly",
                "details": {
                    "suspicious_connections": 3,
                    "data_exfiltration": True
                }
            }
        ],
        "artifacts": [
            {
                "file_path": "C:\\Users\\Test\\Documents\\file1.docx",
                "hash": "a1b2c3d4e5f6g7h8i9j0",
                "operation": "encrypted"
            },
            {
                "file_path": "C:\\Users\\Test\\Documents\\file2.xlsx",
                "hash": "b2c3d4e5f6g7h8i9j0k1",
                "operation": "encrypted"
            },
            {
                "file_path": "C:\\Users\\Test\\Documents\\READ_ME.txt",
                "hash": "c3d4e5f6g7h8i9j0k1l2",
                "operation": "created"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/event",
            json=case_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Caso personalizado creado exitosamente!")
            print(f"   Case ID: {data.get('case_id')}")
            print(f"   Eventos guardados: {data.get('events_saved', 0)}")
            print(f"   Artefactos guardados: {data.get('artifacts_saved', 0)}")
            return data.get('case_id')
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5001")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def list_cases():
    """Lista todos los casos"""
    print("\n📋 Listando todos los casos...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/cases")
        
        if response.status_code == 200:
            cases = response.json()
            if cases:
                print(f"✅ Se encontraron {len(cases)} caso(s):")
                for case in cases:
                    print(f"\n   Caso ID: {case.get('id')}")
                    print(f"   Severidad: {case.get('severity')}")
                    print(f"   Proceso: {case.get('process_name')}")
                    print(f"   Fecha: {case.get('detected_at')}")
                    print(f"   Estado: {case.get('status')}")
            else:
                print("⚠️ No hay casos en la base de datos")
            return cases
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def show_case_details(case_id):
    """Muestra los detalles de un caso"""
    print(f"\n🔍 Mostrando detalles del caso {case_id}...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/cases/{case_id}")
        
        if response.status_code == 200:
            case = response.json()
            print(f"✅ Detalles del caso {case_id}:")
            print(json.dumps(case, indent=2, ensure_ascii=False))
            return case
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("🧪 TEST DE CREACIÓN DE CASOS - CyberGuard Backend")
    print("=" * 60)
    
    # 1. Verificar que el servidor está corriendo
    print("\n1️⃣ Verificando conexión con el servidor...")
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=2)
        if response.status_code == 200:
            print("✅ Servidor está corriendo")
        else:
            print("⚠️ Servidor responde pero con error")
    except:
        print("❌ No se pudo conectar al servidor")
        print("   Por favor, inicia el servidor con: python backend/server_local.py")
        return
    
    # 2. Crear caso de prueba rápido
    case_id_1 = create_test_case()
    
    # 3. Crear caso personalizado
    case_id_2 = create_custom_case()
    
    # 4. Listar todos los casos
    cases = list_cases()
    
    # 5. Mostrar detalles del primer caso
    if case_id_1:
        show_case_details(case_id_1)
    
    # 6. Mostrar URLs útiles
    print("\n" + "=" * 60)
    print("📌 URLs útiles:")
    print("=" * 60)
    print(f"   Ver todos los casos: {BACKEND_URL}/cases")
    if case_id_1:
        print(f"   Ver detalles caso {case_id_1}: {BACKEND_URL}/cases/{case_id_1}")
        print(f"   Ver reporte caso {case_id_1}: {BACKEND_URL}/report/{case_id_1}")
    if case_id_2:
        print(f"   Ver detalles caso {case_id_2}: {BACKEND_URL}/cases/{case_id_2}")
        print(f"   Ver reporte caso {case_id_2}: {BACKEND_URL}/report/{case_id_2}")
    print("=" * 60)

if __name__ == "__main__":
    main()

