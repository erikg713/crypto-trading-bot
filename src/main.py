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

