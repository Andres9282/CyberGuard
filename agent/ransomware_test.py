# agent/ransomware_test.py
# Simulador de ataque ransomware para pruebas

import os
import time
import random
import string
from pathlib import Path

def generate_random_extension():
    """Genera una extensión aleatoria para simular cifrado"""
    extensions = ['.encrypted', '.locked', '.crypto', '.ransom']
    return random.choice(extensions)

def simulate_ransomware_attack(target_folder, num_files=10, delay=0.1):
    """
    Simula un ataque ransomware modificando archivos en la carpeta objetivo.
    
    Args:
        target_folder: Ruta de la carpeta a atacar
        num_files: Número de archivos a modificar
        delay: Retraso entre modificaciones (segundos)
    """
    target_path = Path(target_folder)
    
    if not target_path.exists():
        print(f"⚠️ Creando carpeta objetivo: {target_folder}")
        target_path.mkdir(parents=True, exist_ok=True)
    
    # Buscar archivos existentes
    existing_files = list(target_path.glob("**/*"))
    existing_files = [f for f in existing_files if f.is_file()]
    
    if not existing_files:
        print("⚠️ No hay archivos en la carpeta. Creando archivos de prueba...")
        for i in range(num_files):
            test_file = target_path / f"test_file_{i}.txt"
            test_file.write_text(f"Contenido original del archivo {i}\n")
        existing_files = list(target_path.glob("*.txt"))
    
    print(f" Iniciando simulación de ataque ransomware...")
    print(f" Carpeta objetivo: {target_folder}")
    print(f" Archivos a modificar: {len(existing_files[:num_files])}")
    
    modified_count = 0
    for file_path in existing_files[:num_files]:
        try:
            # Leer contenido original
            original_content = file_path.read_bytes()
            
            # Simular cifrado: agregar extensión y modificar contenido
            new_extension = generate_random_extension()
            new_name = file_path.stem + new_extension
            
            # Crear nuevo archivo "cifrado"
            encrypted_path = file_path.parent / new_name
            encrypted_path.write_bytes(original_content + b"\n[ENCRYPTED BY RANSOMWARE]")
            
            # Eliminar archivo original
            file_path.unlink()
            
            modified_count += 1
            print(f"   {file_path.name} → {new_name}")
            
            time.sleep(delay)
            
        except Exception as e:
            print(f"   Error procesando {file_path}: {e}")
    
    print(f"\n Ataque simulado completado: {modified_count} archivos modificados")
    return modified_count

if __name__ == "__main__":
    import sys
    
    # Obtener carpeta objetivo desde argumentos o variable de entorno
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
    else:
        target_folder = os.getenv(
            "CYBERGUARD_WATCH_FOLDER",
            "/home/andres/attack_test" if os.name != 'nt' else "C:\\attack_test"
        )
    
    num_files = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    
    simulate_ransomware_attack(target_folder, num_files, delay)

