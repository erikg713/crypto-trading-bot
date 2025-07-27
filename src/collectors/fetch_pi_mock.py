# src/collectors/fetch_pi_mock.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_mock_pi_ohlcv(interval="15m", periods=500):
    now = datetime.utcnow()
    dt = pd.date_range(end=now, periods=periods, freq=interval.upper())
    data = {
        "timestamp": dt,
        "open": np.random.uniform(0.01, 0.03, size=periods),
        "high": np.random.uniform(0.03, 0.05, size=periods),
        "low": np.random.uniform(0.01, 0.03, size=periods),
        "close": np.random.uniform(0.02, 0.04, size=periods),
        "volume": np.random.uniform(100, 1000, size=periods),
    }
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df[["open", "high", "low", "close", "volume"]]

# Example usage
if __name__ == "__main__":
    df = fetch_mock_pi_ohlcv()
    print(df.tail())