import os
from alpaca_trade_api.rest import REST

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")
BASE_URL = "https://paper-api.alpaca.markets"

client = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version='v2')

def place_order(symbol, qty, side, type='market', time_in_force='gtc'):
    try:
        order = client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            time_in_force=time_in_force
        )
        return order
    except Exception as e:
        print(f"Alpaca order failed: {e}")
        return None

