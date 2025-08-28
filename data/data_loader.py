# data/data_loader.py
import pandas as pd

def load_historical_prices(filepath: str = "historical_prices.csv") -> pd.DataFrame:
    """Load OHLCV data into a DataFrame, sorted by date."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    df.sort_values("date", inplace=True)
    return df
