import ta
import pandas as pd
from src.features.indicators import add_indicators
import yaml

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

def generate_features(df: pd.DataFrame):
    df = add_indicators(df)
    shift = config["model"]["target_shift"]
    df['target'] = (df['close'].shift(-shift) > df['close']).astype(int)
    df.dropna(inplace=True)

    features = df[['rsi', 'ema_10', 'macd']]
    labels = df['target']
    return features, labels

def generate_features(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    df['ema_10'] = ta.trend.EMAIndicator(df['close'], window=10).ema_indicator()
    df['macd'] = ta.trend.MACD(df['close']).macd()

    df['target'] = (df['close'].shift(-3) > df['close']).astype(int)  # Predict rise in next 3 steps
    df.dropna(inplace=True)
    features = df[['rsi', 'ema_10', 'macd']]
    labels = df['target']
    return features, labels

