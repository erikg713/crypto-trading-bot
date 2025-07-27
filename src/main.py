# src/main.py

import time
from src.learners.predict_signals import predict
from src.executors.trade_manager import execute_trade
from src.executors.risk_controls import validate_risk
from src.collectors.binance_client import get_binance_client
from src.collectors.fetch_historical import fetch_ohlcv
from src.models.predictor import TradingModel

def prepare_features(df):
    # Example feature engineering — replace with the actual features used for training
    df["return"] = df["close"].pct_change()
    df["ma5"] = df["close"].rolling(window=5).mean()
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["volatility"] = df["close"].rolling(window=10).std()
    df = df.dropna()

    return df[["return", "ma5", "ma20", "volatility"]]

def main():
    print("📈 Fetching OHLCV for BTCUSDT...")
    df = fetch_ohlcv("BTCUSDT", interval="15m", limit=100)
    features = prepare_features(df)

    print("🤖 Loading trading model...")
    model = TradingModel()

    print("🔮 Making predictions...")
    prediction = model.predict(features)
    print(prediction[-10:])  # Show last 10 predictions

# Parameters
SYMBOL = "BTCUSDT"
QUANTITY = 0.001  # Adjust based on asset and risk
INTERVAL_SECONDS = 60 * 15  # Every 15 minutes

def get_available_usdt():
    client = get_binance_client()
    balances = client.get_asset_balance(asset='USDT')
    return float(balances['free'])

def run_bot():
    print("🚀 Starting Crypto Trading Bot...")

    while True:
        try:
            print("\n🔎 Checking market signal...")
            action, confidence = predict()
            print(f"Decision: {action.upper()} | Confidence: {confidence:.2f}")

            if action == "buy":
                usdt = get_available_usdt()
                if validate_risk(usdt, QUANTITY * 20000):  # Approximate price scaling
                    execute_trade(SYMBOL, action, QUANTITY)
                else:
                    print("🛑 Trade skipped due to risk constraints.")
            else:
                print("💤 Holding position. No action taken.")

        except Exception as e:
            print(f"❌ ERROR: {e}")

        print(f"⏳ Waiting {INTERVAL_SECONDS // 60} minutes...\n")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    run_bot()

import time
from src.learners.predict_signals import get_latest_signal
from src.executors.trade_manager import place_order
import time
from src.learners.predict_signals import get_latest_signal
from src.executors.trade_manager import place_order
import yaml

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

INTERVAL_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
}

def run_bot():
    interval = config["trade"]["interval"]
    sleep_time = INTERVAL_SECONDS.get(interval, 900)
    threshold = config["trade"]["confidence_threshold"]

    while True:
        signal, confidence = get_latest_signal()
        print(f"Signal: {signal} | Confidence: {confidence:.2f}")
        if signal == 1 and confidence >= threshold:
            place_order(signal)
        else:
            print("⚠️ Confidence too low or no signal.")

        time.sleep(sleep_time)

if __name__ == "__main__":
    run_bot()

while True:
    signal, confidence = get_latest_signal()
    if signal == 1 and confidence > 0.75:
        place_order(signal)
    else:
        print(f"Hold — Confidence: {confidence:.2f}")
    time.sleep(900)  # Run every 15 mins

