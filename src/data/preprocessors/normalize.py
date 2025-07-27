# src/data/preprocessors/normalize.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_features(df: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[feature_cols])
    scaled_df = pd.DataFrame(scaled, columns=feature_cols, index=df.index)
    return scaled_df
