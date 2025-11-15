# ml/features.py
from pathlib import Path
import os
import time


# ==============================
#    FEATURE EXTRACTOR
# ==============================

def extract_features(folder):
    """
    Extrae características simples y robustas de la carpeta monitoreada,
    compatibles con Windows y sin necesidad de watchdog.
    """

    folder = Path(folder)
    if not folder.exists():
        return {
            "size_change": 0,
            "created": 0,
            "deleted": 0,
            "encrypted": 0,
            "rapid_changes": 0
        }

    total_size = 0
    encrypted = 0
    created = 0
    deleted = 0

    # Contar archivos
    files = list(folder.glob("*"))

    # Tamaño total
    for f in files:
        try:
            total_size += f.stat().st_size

            # heurística simple de archivos cifrados:
            # extensiones sospechosas:
            if f.suffix.lower() in [".locked", ".enc", ".encrypted"]:
                encrypted += 1

            # extensiones renombradas (simulan ransomware)
            if f.suffix.lower() not in [".txt", ".pdf", ".jpg", ".png"]:
                if len(f.suffix) > 6:
                    encrypted += 1

        except:
            pass

    # Heurística básica:
    created = len(files)

    # rapid_changes: entre 0 y 300
    # Si hay muchos archivos → más riesgo
    rapid_changes = min(created * 2, 300)

    # size_change: escala proporcional al peso
    size_change = min(int(total_size / 1024), 2000)

    return {
        "size_change": size_change,
        "created": created,
        "deleted": deleted,
        "encrypted": encrypted,
        "rapid_changes": rapid_changes
    }
