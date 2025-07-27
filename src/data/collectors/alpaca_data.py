# src/data/collectors/alpaca_data.py

from src.api_clients.alpaca_client import get_alpaca_client
import pandas as pd

def fetch_stock_ohlcv(symbol="AAPL", timeframe="1D", limit=100) -> pd.DataFrame:
    client = get_alpaca_client()
    barset = client.get_bars(symbol, timeframe, limit=limit)
    data = barset.df[symbol]

    df = pd.DataFrame()
    df["timestamp"] = data.index
    df["open"] = data["open"]
    df["high"] = data["high"]
    df["low"] = data["low"]
    df["close"] = data["close"]
    df["volume"] = data["volume"]

    df.set_index("timestamp", inplace=True)
    return df
