from binance.client import Client
import os

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

def get_binance_client():
    if not API_KEY or not API_SECRET:
        raise ValueError("Binance API credentials not found in environment variables")
    client = Client(API_KEY, API_SECRET)
    return client

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

