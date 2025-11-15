# agent/monitor.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests
from backend.config import FOLDER_TO_WATCH, BACKEND_URL
from ml.features import extract_features   # crea features

class AttackHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        features = extract_features(event)

        print("📂 Cambio detectado:", event.src_path)
        print("🔍 Features:", features)

        requests.post(BACKEND_URL, json={"features": features})

def start_monitor():
    observer = Observer()
    handler = AttackHandler()
    observer.schedule(handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()
    print(f"👀 Monitoreando carpeta: {FOLDER_TO_WATCH}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitor()
