from src.main import get_latest_signal
from src.executors.trade_manager import place_order

def test_end_to_end_decision():
    signal, confidence = get_latest_signal()
    if signal == 1:
        place_order(signal)

