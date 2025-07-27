from binance.client import Client
import os

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def place_order(symbol, side, quantity, order_type='MARKET'):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        return order
    except Exception as e:
        print(f"Binance order failed: {e}")
        return None

