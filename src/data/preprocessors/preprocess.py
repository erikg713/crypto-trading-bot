# src/data/preprocessors/preprocess.py

import pandas as pd

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds simple technical indicators to the dataframe.
    Assumes df has columns: 'open', 'high', 'low', 'close', 'volume'
    """
    df = df.copy()
    df['return'] = df['close'].pct_change()
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['volatility'] = df['close'].rolling(window=10).std()
    df.dropna(inplace=True)
    return df
