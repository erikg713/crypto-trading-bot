from binance.client import Client
import os
from src.collectors.binance_client import client
import yaml
# src/executors/trade_manager.py

from binance.enums import *
from src.collectors.binance_client import get_binance_client

client = get_binance_client()

def execute_trade(symbol: str, action: str, quantity: float):
    if action == "buy":
        print(f"🔼 Placing BUY order: {symbol} {quantity}")
        return client.order_market_buy(symbol=symbol, quantity=quantity)

    elif action == "sell":
        print(f"🔽 Placing SELL order: {symbol} {quantity}")
        return client.order_market_sell(symbol=symbol, quantity=quantity)

    else:
        print(f"⚪ No trade executed (action: {action})")
        return None
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

