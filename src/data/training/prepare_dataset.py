# src/data/training/prepare_dataset.py

import pandas as pd
from src.data.preprocessors.preprocess import add_technical_indicators
from src.data.preprocessors.normalize import normalize_features

def prepare_dataset(df: pd.DataFrame, label_col: str = 'close', horizon: int = 1):
    """
    Prepares dataset for training: adds indicators, normalizes, and generates labels.
    """
    df = add_technical_indicators(df)

    # Generate target: 1 if price goes up after horizon steps, else 0
    df['target'] = (df[label_col].shift(-horizon) > df[label_col]).astype(int)

    # Normalize feature columns
    feature_cols = ['return', 'ma5', 'ma20', 'volatility']
    df = df.dropna()
    features = normalize_features(df, feature_cols)

    return features, df['target']
