# src/learners/predict_signals.py

import joblib
from src.features.feature_engineer import generate_features
from src.collectors.fetch_historical import fetch_ohlcv

MODEL_PATH = "models/signal_model.pkl"

def load_model():
    """Load the trained signal prediction model."""
    return joblib.load(MODEL_PATH)

def generate_live_features(symbol="BTCUSDT", interval="15m", limit=40):
    """
    Fetch recent OHLCV data and generate features.
    Returns the features DataFrame for prediction.
    """
    df = fetch_ohlcv(symbol=symbol, interval=interval, limit=limit)
    X, _ = generate_features(df)
    return X

def predict():
    """
    Load model, generate features for latest data, 
    and return the predicted action and confidence score.
    """
    model = load_model()
    X_live = generate_live_features()
    latest_features = X_live.iloc[[-1]]  # Take last row for current state

    prediction = model.predict(latest_features)[0]
    confidence = model.predict_proba(latest_features)[0].max()

    action = "buy" if prediction == 1 else "hold"
    return action, confidence

if __name__ == "__main__":
    action, conf = predict()
    print(f"Action: {action.upper()} with confidence: {conf:.2f}")
