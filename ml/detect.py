# ml/detect.py
import pickle
import numpy as np
from .paths import MODEL_FILE


class AnomalyDetector:
    """
    Wrapper sobre el modelo entrenado (Isolation Forest).
    Carga el modelo una sola vez y expone un método detect().
    """

    def __init__(self, model_path=MODEL_FILE):
        if not model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo entrenado: {model_path}\n"
                f"Primero ejecuta: python -m ml.train_model"
            )
        with model_path.open("rb") as f:
            self.model = pickle.load(f)

    def detect(self, features):
        """
        features: lista de floats [files, cpu, processes]
        return: True si es anomalía, False si es normal
        """
        X = np.array([features], dtype=float)
        pred = self.model.predict(X)  # -1 = anomalía, 1 = normal
        return pred[0] == -1


# --------- INSTANCIA GLOBAL + FUNCIÓN DE CONVENIENCIA ---------

_detector = None


def get_detector():
    """
    Devuelve una instancia global de AnomalyDetector,
    para reutilizar el modelo sin recargarlo cada vez.
    """
    global _detector
    if _detector is None:
        _detector = AnomalyDetector()
    return _detector


def detect_anomaly(features):
    """
    Función simple que el agente puede importar:
    from ml.detect import detect_anomaly
    """
    detector = get_detector()
    return detector.detect(features)


# --------- BLOQUE DE PRUEBA MANUAL ---------

if __name__ == "__main__":
    # TEST usando datos REALES del baseline
    import json
    from .paths import BASELINE_FILE

    with BASELINE_FILE.open("r", encoding="utf-8") as f:
        baseline = json.load(f)

    normal_sample = baseline[0]  # primera muestra real
    files, cpu, procs = normal_sample

    # Creamos una muestra artificialmente "agresiva"
    attack_sample = [
        files + 200,           # muchos más archivos
        min(cpu + 70, 100),    # CPU casi al 100%
        procs + 200            # muchos más procesos
    ]

    print("Muestra baseline original:", normal_sample)
    print("Normal test (esperado False):", detect_anomaly(normal_sample))
    print("Attack test (esperado True):", detect_anomaly(attack_sample))
