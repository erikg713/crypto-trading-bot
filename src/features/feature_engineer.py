import ta
import pandas as pd

def generate_features(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    df['ema_10'] = ta.trend.EMAIndicator(df['close'], window=10).ema_indicator()
    df['macd'] = ta.trend.MACD(df['close']).macd()

    df['target'] = (df['close'].shift(-3) > df['close']).astype(int)  # Predict rise in next 3 steps
    df.dropna(inplace=True)
    features = df[['rsi', 'ema_10', 'macd']]
    labels = df['target']
    return features, labels

