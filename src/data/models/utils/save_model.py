import joblib
import os

def save_model(model, filename, directory="src/data/models/checkpoints/"):
    os.makedirs(directory, exist_ok=True)
    full_path = os.path.join(directory, filename)
    joblib.dump(model, full_path)
    print(f"✅ Model saved to {full_path}")
    return full_path

