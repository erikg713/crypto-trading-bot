import joblib
import os

def load_model(filename, directory="src/data/models/checkpoints/"):
    full_path = os.path.join(directory, filename)
    model = joblib.load(full_path)
    print(f"📦 Model loaded from {full_path}")
    return model

