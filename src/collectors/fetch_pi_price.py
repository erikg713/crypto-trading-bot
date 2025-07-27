import requests
import pandas as pd
from datetime import datetime

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