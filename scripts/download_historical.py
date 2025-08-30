import pandas as pd
from binance.client import Client
from pathlib import Path
import time

# ---------------------------
# CONFIGURATION
# ---------------------------
DATA_DIR = Path("data/raw/market")
DATA_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = ""       # Optional; leave empty for public access
API_SECRET = ""

client = Client(API_KEY, API_SECRET)

SYMBOLS = ["ETHUSDT", "SOLUSDT"]
INTERVALS = ["1h", "1d"]  # Add "1m", "5m" if needed
LIMIT = 1000              # Max candles per API call

# ---------------------------
# FETCH FUNCTION
# ---------------------------
def fetch_all_klines(symbol: str, interval: str):
    csv_file = DATA_DIR / f"{symbol}_{interval}.csv"

    # Load existing data if available
    if csv_file.exists():
        df_existing = pd.read_csv(csv_file, parse_dates=["open_time"])
        start_ts = int(df_existing["open_time"].max().timestamp() * 1000) + 1
        print(f"[INFO] Resuming {symbol} ({interval}) from {df_existing['open_time'].max()}")
    else:
        df_existing = pd.DataFrame()
        start_ts = None
        print(f"[INFO] Fetching full history for {symbol} ({interval})")

    all_data = []

    while True:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=LIMIT, startTime=start_ts)
        if not klines:
            break

        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df = df[["open_time", "open", "high", "low", "close", "volume"]]
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        # Remove duplicates
        if not df_existing.empty:
            df = df[~df["open_time"].isin(df_existing["open_time"])]

        if df.empty:
            break

        all_data.append(df)
        start_ts = int(df["open_time"].max().timestamp() * 1000) + 1
        time.sleep(0.5)  # avoid API rate limits

    if all_data:
        df_all = pd.concat(all_data)
        if not df_existing.empty:
            df_all = pd.concat([df_existing, df_all])
        df_all = df_all.sort_values("open_time").reset_index(drop=True)
        df_all.to_csv(csv_file, index=False)
        print(f"[INFO] Saved {len(df_all)} rows to {csv_file}")
    else:
        print(f"[INFO] No new data to fetch for {symbol} ({interval})")

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            fetch_all_klines(symbol, interval)
