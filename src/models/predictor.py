import os
import pickle
import pandas as pd
from sklearn.base import BaseEstimator
from typing import Union

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_v1.pkl")

class TradingModel:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model: Union[BaseEstimator, None] = None
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        print(f"✅ Loaded model from: {self.model_path}")

    def predict(self, features: pd.DataFrame):
        if self.model is None:
            raise Exception("Model not loaded.")
        return self.model.predict(features)

    def predict_proba(self, features: pd.DataFrame):
        if self.model is None:
            raise Exception("Model not loaded.")
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(features)
        else:
            raise Exception("Model does not support probability prediction.")
