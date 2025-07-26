from binance.client import Client
import os
from src.collectors.binance_client import client
import yaml

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

def place_order(signal):
    symbol = config["trade"]["symbol"]
    quantity = config["trade"]["trade_amount"]

    if signal == 1:
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print(f"✅ Buy Order Executed: {order}")
    else:
        print("🟡 Hold / No trade executed.")

client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET"))

def place_order(signal):
    if signal == 1:
        order = client.order_market_buy(symbol="BTCUSDT", quantity=0.001)
        print(f"Buy Order Executed: {order}")
    else:
        print("No action taken.")

