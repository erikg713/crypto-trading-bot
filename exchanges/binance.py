# exchanges/binance.py

import os
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from exchanges.base_exchange import BaseExchange

# ---------------------------
# Binance API Client
# ---------------------------
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)


def fetch_historical_klines(symbol: str, interval: str = "1d", start: str = "1 Jul, 2024", end: str = None) -> pd.DataFrame:
    """Fetch historical OHLCV data from Binance."""
    try:
        print(f"[INFO] Fetching {symbol} data from Binance...")
        klines = client.get_historical_klines(symbol, interval, start, end)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        numeric_cols = ["open", "high", "low", "close", "volume"]
        df[numeric_cols] = df[numeric_cols].astype(float)
        return df[["timestamp", "open", "high", "low", "close", "volume"]]
    except (BinanceAPIException, BinanceRequestException) as e:
        print(f"[ERROR] Binance API error: {e}")
        return pd.DataFrame()


def save_to_csv(df: pd.DataFrame, symbol: str, raw_dir: str = "data/raw/market") -> str:
    """Save OHLCV dataframe to CSV."""
    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"{symbol}.csv")
    df.to_csv(file_path, index=False)
    print(f"[INFO] Saved {symbol} data to {file_path}")
    return file_path


# ---------------------------
# Binance Exchange Wrapper
# ---------------------------
class BinanceExchange(BaseExchange):
    """Wrapper class for trading via Binance."""
    
    def get_market_data(self):
        """Fetch current market price (replace with API call)."""
        # Example placeholder; replace with real Binance price fetch
        return {"close": 300.0}

    def buy(self, amount=None):
        """Execute a buy order."""
        print("Binance BUY", f"Amount: {amount}")

    def sell(self, amount=None):
        """Execute a sell order."""
        print("Binance SELL", f"Amount: {amount}")

    def close_position(self):
        """Close current position."""
        print("Binance CLOSE POSITION")


# ---------------------------
# Example run
# ---------------------------
if __name__ == "__main__":
    df = fetch_historical_klines("SOLUSDT", "1d", "1 Jul, 2024")
    if not df.empty:
        save_to_csv(df, "SOLUSDT")
