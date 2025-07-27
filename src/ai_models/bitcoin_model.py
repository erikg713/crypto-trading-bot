# src/ai_models/bitcoin_model.py

import pandas as pd
import joblib
import os

MODEL_PATH = "models/btc_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def prepare_features(df: pd.DataFrame):
    df["return"] = df["close"].pct_change()
    df["ma5"] = df["close"].rolling(window=5).mean()
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["volatility"] = df["close"].rolling(window=10).std()
    df = df.dropna()
    return df[["return", "ma5", "ma20", "volatility"]]

def predict(symbol: str, df: pd.DataFrame) -> int:
    model = load_model()
    features = prepare_features(df)
    pred = model.predict(features)[-1]  # last prediction
    return int(pred)

def predict(df):
    # Dummy strategy: buy if last close > previous close else sell
    if len(df) < 2:
        return 0
    if df['close'].iloc[-1] > df['close'].iloc[-2]:
        return 1  # buy
    else:
        return -1  # sell

