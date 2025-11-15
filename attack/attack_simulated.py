from pathlib import Path
import time
import os

FOLDER = Path.home() / "victim_data"

def simulate_attack():
    print("🔥 Iniciando ataque simulado...")

    FOLDER.mkdir(exist_ok=True)

    # generar muchos archivos para activar el agente
    for i in range(40):
        file_path = FOLDER / f"encrypted_{i}.txt"
        with open(file_path, "w") as f:
            f.write("RANSOMWARE TEST DATA\n" * 10)
        time.sleep(0.05)

    # sobrescribir archivos existentes (simula cifrado)
    for f in FOLDER.glob("*.txt"):
        with open(f, "a") as file:
            file.write("### ENCRYPTED ###\n")

    # mensaje de rescate
    ransom_note = FOLDER / "README_RESTORE_FILES.txt"
    with open(ransom_note, "w") as f:
        f.write(
            "Tus archivos han sido cifrados.\n"
            "Paga 1 BTC para recuperarlos.\n"
        )

    print("🚨 Ataque completado.")

if __name__ == "__main__":
    simulate_attack()
