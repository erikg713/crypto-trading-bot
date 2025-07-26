from binance.client import Client
import os

client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET"))

def place_order(signal):
    if signal == 1:
        order = client.order_market_buy(symbol="BTCUSDT", quantity=0.001)
        print(f"Buy Order Executed: {order}")
    else:
        print("No action taken.")

