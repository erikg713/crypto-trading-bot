# src/data/collectors/binance_data.py

from src.api_clients.binance_client import get_binance_client
import pandas as pd

def fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=500) -> pd.DataFrame:
    client = get_binance_client()
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    float_cols = ["open", "high", "low", "close", "volume"]
    df[float_cols] = df[float_cols].astype(float)
    return df[float_cols]

