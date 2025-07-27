# src/ai_models/options_model.py

import pandas as pd
import joblib
import os

MODEL_PATH = "models/options_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def prepare_features(df: pd.DataFrame):
    # Example features for options pricing
    df["return"] = df["close"].pct_change()
    df["iv_mean"] = df["implied_volatility"].rolling(window=5).mean()
    df = df.dropna()
    return df[["return", "iv_mean"]]

def predict(symbol: str, df: pd.DataFrame) -> str:
    model = load_model()
    features = prepare_features(df)
    pred = model.predict(features)[-1]

    if pred == 1:
        return "buy"
    elif pred == -1:
        return "sell"
    else:
        return "hold"
