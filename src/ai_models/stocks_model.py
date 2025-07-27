def predict(symbol, df):
    """
    Dummy model: buy if close last > previous; sell if opposite.
    """
    if len(df) < 2:
        return 0
    if df['close'].iloc[-1] > df['close'].iloc[-2]:
        return 'buy'
    else:
        return 'sell'

