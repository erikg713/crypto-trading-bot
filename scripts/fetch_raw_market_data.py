import pandas as pd
from binance.client import Client
from pathlib import Path
import os
import time

# ---------------------------
# CONFIGURATION
# ---------------------------
DATA_DIR = Path("data/raw/market")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# If you want to use Binance API keys, insert them here. Otherwise, anonymous requests work for historical klines.
API_KEY = ""
API_SECRET = ""

client = Client(API_KEY, API_SECRET)

# Trading pairs to fetch
SYMBOLS = ["ETHUSDT", "SOLUSDT"]

# Interval options: "1m", "5m", "15m", "1h", "1d"
INTERVAL = "1h"

# Number of candles to fetch per request (max 1000)
LIMIT = 1000

# ---------------------------
# FUNCTIONS
# ---------------------------
def fetch_symbol(symbol: str, interval: str = "1h", limit: int = 1000) -> pd.DataFrame:
    """Fetch OHLCV historical data for a single symbol."""
    print(f"[INFO] Fetching {symbol}...")
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df = df[["open_time", "open", "high", "low", "close", "volume"]]
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df

def save_symbol(df: pd.DataFrame, symbol: str):
    """Save symbol OHLCV to CSV."""
    path = DATA_DIR / f"{symbol}.csv"
    df.to_csv(path, index=False)
    print(f"[INFO] Saved {symbol} data to {path}")

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    for symbol in SYMBOLS:
        df = fetch_symbol(symbol, interval=INTERVAL, limit=LIMIT)
        save_symbol(df, symbol)
        time.sleep(1)  # avoid hitting API limits
