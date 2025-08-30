# exchanges/binance.py

import os
import time
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

# Binance credentials (optional if public endpoints only)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# Initialize client
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)


def fetch_historical_klines(symbol: str, interval: str = "1d", start: str = "1 Jul, 2024", end: str = None) -> pd.DataFrame:
    """
    Fetch historical kline/candlestick data from Binance.

    :param symbol: Trading pair symbol, e.g., 'SOLUSDT'
    :param interval: Interval string ('1m','5m','1h','1d')
    :param start: Start date (string like "1 Jul, 2024")
    :param end: End date (string or None)
    :return: Pandas DataFrame with OHLCV data
    """
    try:
        print(f"[INFO] Fetching {symbol} data from Binance...")
        klines = client.get_historical_klines(symbol, interval, start, end)

        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])

        # Convert datatypes
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        numeric_cols = ["open", "high", "low", "close", "volume"]
        df[numeric_cols] = df[numeric_cols].astype(float)

        # Keep only necessary columns
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]

        return df

    except (BinanceAPIException, BinanceRequestException) as e:
        print(f"[ERROR] Binance API error: {e}")
        return pd.DataFrame()


def save_to_csv(df: pd.DataFrame, symbol: str, raw_dir: str = "data/raw/market") -> str:
    """
    Save dataframe to CSV file inside raw/market folder.

    :param df: Pandas DataFrame with OHLCV data
    :param symbol: Trading pair symbol
    :param raw_dir: Folder path to save CSV
    :return: File path of saved CSV
    """
    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"{symbol}.csv")
    df.to_csv(file_path, index=False)
    print(f"[INFO] Saved {symbol} data to {file_path}")
    return file_path


if __name__ == "__main__":
    # Example run: fetch & save SOLUSDT daily candles
    df = fetch_historical_klines("SOLUSDT", "1d", "1 Jul, 2024")
    if not df.empty:
        save_to_csv(df, "SOLUSDT")

from exchanges.base_exchange import BaseExchange

class BinanceExchange(BaseExchange):
    def get_market_data(self):
        return {"close": 300.0}  # Replace with Binance API call

    def buy(self):
        print("Binance BUY")

    def sell(self):
        print("Binance SELL")

    def close_position(self):
        print("Binance CLOSE")
