import ta

def add_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    df['ema_10'] = ta.trend.EMAIndicator(df['close'], window=10).ema_indicator()
    df['macd'] = ta.trend.MACD(df['close']).macd()
    return df

