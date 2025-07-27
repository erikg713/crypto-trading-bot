from binance.client import Client
import pandas as pd
import os
from src.collectors.binance_client import client
import pandas as pd
from datetime import datetime
from src.collectors.binance_client import get_binance_client
import requests
import pandas as pd
from datetime import datetime

def fetch_pi_ohlcv(vs_currency: str = "usd", days: int = 30, interval: str = "daily") -> pd.DataFrame:
    """
    Fetch historical OHLC data for Pi Network (PI) from CoinGecko.

    :param vs_currency: Comparison currency, default "usd".
    :param days: Number of days of history. Can be "max".
    :param interval: "daily" or "hourly".
    :return: pandas DataFrame indexed by timestamp with columns open, high, low, close, volume.
    """
    base = "https://api.coingecko.com/api/v3/coins/pi-network/ohlc"
    params = {"vs_currency": vs_currency, "days": days}
    resp = requests.get(base, params=params)
    resp.raise_for_status()
    data = resp.json()

    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    # CoinGecko OHLC endpoint does not include volume — fetch volume separately:
    # Use /market_chart endpoint
    market_url = f"https://api.coingecko.com/api/v3/coins/pi-network/market_chart"
    mresp = requests.get(market_url, params={"vs_currency": vs_currency, "days": days})
    mresp.raise_for_status()
    market_data = mresp.json()
    volumes = market_data["total_volumes"]

    vol_df = pd.DataFrame(volumes, columns=["timestamp", "volume"])
    df = pd.merge(df, vol_df, on="timestamp", how="left")

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df[["open", "high", "low", "close", "volume"]]


# Example usage
if __name__ == "__main__":
    df = fetch_pi_ohlcv(days=7)
    print(df.tail())
def fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=500):
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

# Example usage
if __name__ == "__main__":
    df = fetch_ohlcv()
    print(df.tail())
def fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=1000):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades', 
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_SECRET"))

def fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=1000):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades', 
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

