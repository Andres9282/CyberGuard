# ml/features.py
import psutil
import os
from pathlib import Path

def extract_features(attack_folder=None):
    """
    Devuelve el vector de características uniforme para IA.
    features = [cpu_percent, ram_percent, total_processes, files_in_attack_folder]
    """

    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    processes = len(psutil.pids())

    # contar archivos en la carpeta vigilada
    file_count = 0
    if attack_folder:
        try:
            file_count = len(os.listdir(attack_folder))
        except FileNotFoundError:
            file_count = 0

    return [cpu, ram, processes, file_count]
