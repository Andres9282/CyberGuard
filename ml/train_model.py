# ml/train_model.py
import joblib
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def generate_dataset(n=4000):
    X = []
    y = []

    for _ in range(n):

        # Evento normal
        if random.random() < 0.60:
            size = random.randint(1, 50000)
            created = random.choice([0, 1])
            deleted = 0
            entropy = random.uniform(1, 4)
            rapid = random.randint(1, 4)
            label = 0  # normal

        # Evento sospechoso leve
        elif random.random() < 0.85:
            size = random.randint(50000, 200000)
            created = 1
            deleted = random.choice([0, 1])
            entropy = random.uniform(4, 6)
            rapid = random.randint(5, 12)
            label = 0  # normal todavía

        # Ataque tipo ransomware
        else:
            size = random.randint(300000, 2000000)
            created = 1
            deleted = 1
            entropy = random.uniform(6.5, 8)
            rapid = random.randint(15, 40)
            label = 1  # attack

        X.append([size, created, deleted, entropy, rapid])
        y.append(label)

    return np.array(X), np.array(y)



def train():
    X, y = generate_dataset()
    model = RandomForestClassifier(n_estimators=180)
    model.fit(X, y)

    joblib.dump(model, "ml/model.joblib")
    print("Modelo ML entrenado y guardado correctamente.")


if __name__ == "__main__":
    train()
