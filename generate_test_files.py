# generate_test_files.py
from pathlib import Path

FOLDER = Path.home() / "attack_test"

def main():
    FOLDER.mkdir(parents=True, exist_ok=True)
    print(f"📂 Carpeta objetivo: {FOLDER}")

    for i in range(1, 6):
        file_path = FOLDER / f"test_file_{i}.txt"
        file_path.write_text(f"Este es el archivo de prueba #{i}\n")
        print(f"✅ Creado: {file_path}")

if __name__ == "__main__":
    main()
