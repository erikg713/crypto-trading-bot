"""
mnt/data/src/data/models/checkpoints/model_utils.py
===================================================

Utilities for saving and loading model checkpoints (.pkl files)
"""

import pickle
from pathlib import Path
from typing import Any

CHECKPOINT_DIR = Path(__file__).parent
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def save_model(model: Any, filename: str) -> None:
    """
    Save a model to a pickle file.

    Args:
        model: Any Python object (e.g., trained ML model)
        filename: Name of the file (e.g., 'model_v1.pkl')
    """
    file_path = CHECKPOINT_DIR / filename
    with open(file_path, "wb") as f:
        pickle.dump(model, f)
    print(f"[INFO] Model saved to {file_path}")


def load_model(filename: str) -> Any:
    """
    Load a model from a pickle file.

    Args:
        filename: Name of the file (e.g., 'model_v1.pkl')

    Returns:
        The Python object stored in the checkpoint.
    """
    file_path = CHECKPOINT_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Checkpoint {file_path} does not exist")
    with open(file_path, "rb") as f:
        model = pickle.load(f)
    print(f"[INFO] Model loaded from {file_path}")
    return model


# Example usage
if __name__ == "__main__":
    # Example: Save a dictionary as a model
    dummy_model = {"weights": [0.1, 0.2, 0.3], "bias": 0.05}
    save_model(dummy_model, "model_v1.pkl")

    # Load the model
    loaded_model = load_model("model_v1.pkl")
    print("Loaded model:", loaded_model)
