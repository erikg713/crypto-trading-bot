import requests
import pandas as pd
from datetime import datetime
import requests
import pandas as pd

def fetch_pi_ohlcv(vs_currency: str = "usd", days: int = 30) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for Pi Network from CoinGecko API.
    Returns daily OHLCV data.

    :param vs_currency: Currency to compare against (e.g. "usd").
    :param days: Number of days of historical data.
    :return: DataFrame indexed by timestamp with open, high, low, close, volume.
    """
    base_url = "https://api.coingecko.com/api/v3/coins/pi-network/ohlc"
    params = {
        "vs_currency": vs_currency,
        "days": days,
    }
    resp = requests.get(base_url, params=params)
    resp.raise_for_status()
    ohlc_data = resp.json()

    # OHLC data: [timestamp, open, high, low, close]
    df = pd.DataFrame(ohlc_data, columns=["timestamp", "open", "high", "low", "close"])

    # Get volume data separately from market_chart endpoint
    vol_url = f"https://api.coingecko.com/api/v3/coins/pi-network/market_chart"
    vol_params = {"vs_currency": vs_currency, "days": days}
    vol_resp = requests.get(vol_url, params=vol_params)
    vol_resp.raise_for_status()
    vol_data = vol_resp.json()["total_volumes"]

    vol_df = pd.DataFrame(vol_data, columns=["timestamp", "volume"])

    # Merge OHLC with volume
    df = pd.merge(df, vol_df, on="timestamp", how="left")

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Convert all columns to float
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df[["open", "high", "low", "close", "volume"]]
def fetch_pi_price_from_api():
    url = "https://api.some-pi-bridge.com/v1/price-history"
    response = requests.get(url)
    data = response.json()

    # Suppose the API gives: [{'time': 1727330400, 'open':..., 'high':...}]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("timestamp", inplace=True)
    return df[["open", "high", "low", "close", "volume"]]

# Validate with:
# df = fetch_pi_price_from_api()
# print(df.head())