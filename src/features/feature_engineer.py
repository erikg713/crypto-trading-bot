import pandas as pd
import yaml
from src.features.indicators import add_indicators
from config import config

def generate_features(df: pd.DataFrame):
    df = add_indicators(df)

    shift = config.get("model", {}).get("target_shift", 3)
    features_list = config.get("model", {}).get("feature_columns", ['rsi', 'ema_10', 'macd'])

    df['target'] = (df['close'].shift(-shift) > df['close']).astype(int)
    df.dropna(inplace=True)

    features = df[features_list]
    labels = df['target']

    return features, labels

# Load config once globally
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

def generate_features(df: pd.DataFrame):
    # Add technical indicators via your helper function
    df = add_indicators(df)

    # Get shift value from config, default to 3 if missing
    shift = config.get("model", {}).get("target_shift", 3)

    # Label: 1 if price increases after `shift` steps, else 0
    df['target'] = (df['close'].shift(-shift) > df['close']).astype(int)

    # Drop any NaNs caused by indicators or shift
    df.dropna(inplace=True)

    # Pick relevant features - adjust if your add_indicators adds more
    features = df[['rsi', 'ema_10', 'macd']]
    labels = df['target']

    return features, labels

