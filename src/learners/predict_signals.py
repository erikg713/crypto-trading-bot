import joblib
from src.features.feature_engineer import generate_features
from src.collectors.fetch_historical import fetch_ohlcv
import joblib
from src.collectors.fetch_historical import fetch_ohlcv
from src.features.feature_engineer import generate_features

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

