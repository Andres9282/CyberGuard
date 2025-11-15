# ml/features.py
import os
import psutil
from .paths import NORMAL_LOG_DIR

def extract_features(monitor_folder=None):
    """
    Devuelve un vector de características del estado actual del sistema.
    features = [num_archivos, cpu_percent, num_procesos]
    
    monitor_folder: carpeta a observar. Si es None usa NORMAL_LOG_DIR.
    """
    folder = monitor_folder or NORMAL_LOG_DIR

    # Asegurarse de que la carpeta existe
    os.makedirs(folder, exist_ok=True)

    # 1) Número de archivos en la carpeta
    try:
        files = len(os.listdir(folder))
    except FileNotFoundError:
        files = 0

    # 2) Uso de CPU en %
    cpu = psutil.cpu_percent(interval=0.1)

    # 3) Número de procesos activos
    processes = len(psutil.pids())

    return [files, cpu, processes]
