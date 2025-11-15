# agent/attack_simulator.py
import os
import time
import random
from pathlib import Path

TARGET = Path("C:/attack_test")
TARGET.mkdir(exist_ok=True)

def create_files(n):
    for i in range(n):
        f = TARGET / f"file_{int(time.time()*1000)}_{i}.txt"
        f.write_text("ATAQUE: archivo generado\n")
        print(f"[+] Creado: {f}")
        time.sleep(0.02)

def modify_files():
    files = list(TARGET.glob("*.txt"))
    random.shuffle(files)
    for f in files[:50]:
        f.write_text("ATAQUE: archivo MODIFICADO\n")
        print(f"[!] Modificado: {f}")
        time.sleep(0.01)

def delete_files():
    files = list(TARGET.glob("*.txt"))
    for f in files[:30]:
        try:
            f.unlink()
            print(f"[-] Eliminado: {f}")
        except:
            pass
        time.sleep(0.005)

def ransomware_encrypt():
    files = list(TARGET.glob("*.txt"))
    for f in files[:80]:
        new_name = f.with_suffix(".locked")
        f.rename(new_name)
        print(f"[🔒] Encriptado: {new_name}")
        time.sleep(0.008)

def run_attack():
    print("\n🚨 ATAQUE SIMULADO INICIADO 🚨\n")
    create_files(150)
    modify_files()
    ransomware_encrypt()
    delete_files()
    print("\n✔ ATAQUE SIMULADO COMPLETADO ✔\n")

if __name__ == "__main__":
    run_attack()
