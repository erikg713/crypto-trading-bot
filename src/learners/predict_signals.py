# src/learners/predict_signals.py

import joblib
import pandas as pd
from src.features.feature_engineer import generate_features
from src.collectors.fetch_historical import fetch_ohlcv

MODEL_PATH = "models/signal_model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def generate_live_features():
    # Use most recent 30 candles for prediction
    df = fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=40)
    X, _ = generate_features(df)
    # Use the last row as the current state
    return X.iloc[[-1]]

def predict():
    model = load_model()
    X_live = generate_live_features()
    prediction = model.predict(X_live)[0]
    confidence = model.predict_proba(X_live)[0].max()

    action = "buy" if prediction == 1 else "hold"
    return action, confidence

# Example test run
if __name__ == "__main__":
    action, conf = predict()
    print(f"Action: {action.upper()} with confidence: {conf:.2f}")

import joblib
from src.features.feature_engineer import generate_features
from src.collectors.fetch_historical import fetch_ohlcv
import joblib
from src.collectors.fetch_historical import fetch_ohlcv
from src.features.feature_engineer import generate_features
# predict_signals.py
def predict(live_df):
    model = joblib.load('models/signal_model.pkl')
    X = generate_live_features(live_df)
    return model.predict(X), model.predict_proba(X)
model = joblib.load("models/signal_model.pkl")

def get_latest_signal():
    df = fetch_ohlcv(limit=100)
    X, _ = generate_features(df)
    signal = model.predict(X.tail(1))[0]
    confidence = model.predict_proba(X.tail(1)).max()
    return signal, confidence

model = joblib.load("models/signal_model.pkl")

def get_latest_signal():
    df = fetch_ohlcv("BTCUSDT", limit=50)
    X, _ = generate_features(df)
    signal = model.predict(X.tail(1))
    confidence = model.predict_proba(X.tail(1)).max()
    return signal[0], confidence

