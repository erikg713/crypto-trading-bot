# src/main.py

import time
import yaml
from src.learners.predict_signals import get_latest_signal
from src.executors.trade_manager import place_order
from src.executors.risk_controls import validate_risk
from src.collectors.binance_client import get_binance_client

# Load settings
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

INTERVAL_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
}

SYMBOL = config["trade"]["symbol"]
QUANTITY = config["trade"]["quantity"]
THRESHOLD = config["trade"]["confidence_threshold"]
INTERVAL = config["trade"]["interval"]
SLEEP_TIME = INTERVAL_SECONDS.get(INTERVAL, 900)

def get_available_usdt():
    client = get_binance_client()
    balance = client.get_asset_balance(asset="USDT")
    return float(balance["free"])

def run_bot():
    print("🚀 AI Crypto Trading Bot is running...")

    while True:
        try:
            signal, confidence = get_latest_signal()
            print(f"Signal: {signal} | Confidence: {confidence:.2f}")

            if signal == 1 and confidence >= THRESHOLD:
                usdt = get_available_usdt()
                approx_cost = QUANTITY * 20000  # Adjust based on BTC price
                if validate_risk(usdt, approx_cost):
                    place_order(signal)
                else:
                    print("🛑 Trade rejected by risk control.")
            else:
                print("⏸️ No trade — Holding position.")

        except Exception as e:
            print(f"❌ ERROR: {e}")

        print(f"⏳ Sleeping for {SLEEP_TIME // 60} minutes...\n")
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    run_bot()

