# src/executors/risk_controls.py

from binance.exceptions import BinanceAPIException

MAX_TRADE_USDT = 50  # Max trade per position
MAX_DAILY_TRADES = 20

trade_count = 0

def validate_risk(available_usdt: float, trade_amount: float):
    global trade_count
    if trade_count >= MAX_DAILY_TRADES:
        print("❌ Daily trade limit reached.")
        return False

    if trade_amount > available_usdt:
        print("❌ Not enough USDT balance.")
        return False

    if trade_amount > MAX_TRADE_USDT:
        print("⚠️ Trade capped to $50.")
        return False

    trade_count += 1
    return True
def validate_risk():
    # Check stop-loss, daily exposure, max trades
    return True
