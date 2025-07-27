# src/ai_models/stocks_model.py

import pandas as pd
import joblib
import os

MODEL_PATH = "models/stocks_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def prepare_features(df: pd.DataFrame):
    df["return"] = df["close"].pct_change()
    df["ma10"] = df["close"].rolling(window=10).mean()
    df["ma50"] = df["close"].rolling(window=50).mean()
    df["volatility"] = df["close"].rolling(window=10).std()
    df = df.dropna()
    return df[["return", "ma10", "ma50", "volatility"]]

def predict(symbol: str, df: pd.DataFrame) -> str:
    model = load_model()
    features = prepare_features(df)
    pred = model.predict(features)[-1]

    # Convert numeric prediction to string label
    if pred == 1:
        return "buy"
    elif pred == -1:
        return "sell"
    else:
        return "hold"
