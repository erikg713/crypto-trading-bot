def predict(df):
    # Dummy strategy: buy if last close > previous close else sell
    if len(df) < 2:
        return 0
    if df['close'].iloc[-1] > df['close'].iloc[-2]:
        return 1  # buy
    else:
        return -1  # sell

