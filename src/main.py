import time
from src.learners.predict_signals import get_latest_signal
from src.executors.trade_manager import place_order

while True:
    signal, confidence = get_latest_signal()
    if signal == 1 and confidence > 0.75:
        place_order(signal)
    else:
        print(f"Hold — Confidence: {confidence:.2f}")
    time.sleep(900)  # Run every 15 mins

