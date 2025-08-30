import pandas as pd
from pathlib import Path

# Import your data loaders & preprocess
from data.loader import load_market_data
from data.preprocess import add_features
from data.trades import save_trades

# ---------------------------
# SAMPLE STRATEGY: MA Crossover + RSI
# ---------------------------
def run_strategy(df: pd.DataFrame):
    """
    Generate buy/sell signals based on:
    - Short SMA (10) crosses long SMA (50)
    - RSI oversold/overbought conditions
    """
    df = df.copy()
    df["signal"] = "HOLD"

    for i in range(1, len(df)):
        # Moving Average Crossover
        if df["sma_10"].iloc[i] > df["sma_50"].iloc[i] and df["sma_10"].iloc[i-1] <= df["sma_50"].iloc[i-1]:
            df["signal"].iloc[i] = "BUY"
        elif df["sma_10"].iloc[i] < df["sma_50"].iloc[i] and df["sma_10"].iloc[i-1] >= df["sma_50"].iloc[i-1]:
            df["signal"].iloc[i] = "SELL"

        # RSI filter
        if df["rsi"].iloc[i] < 30:
            df["signal"].iloc[i] = "BUY"
        elif df["rsi"].iloc[i] > 70:
            df["signal"].iloc[i] = "SELL"

    return df

# ---------------------------
# BACKTEST EXECUTION
# ---------------------------
def backtest(symbol="ETHUSDT", interval="1h"):
    print(f"[INFO] Running backtest for {symbol} ({interval})")

    # Load raw market data
    df = load_market_data(f"{symbol}_{interval}.csv")

    # Add features
    df = add_features(df)

    # Run strategy
    df_signals = run_strategy(df)

    # Extract executed trades
    trades = df_signals[df_signals["signal"] != "HOLD"][["timestamp", "signal", "close"]].copy()
    trades.rename(columns={"signal": "side", "close": "price"}, inplace=True)
    trades["symbol"] = symbol
    trades["size"] = 1.0  # Example: 1 unit per trade
    trades["pnl"] = 0.0   # Placeholder, PnL can be computed after

    # Save trades
    save_trades(trades)
    print(f"[INFO] Backtest completed. {len(trades)} trades generated.")

    return trades

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    symbols = ["ETHUSDT", "SOLUSDT"]
    interval = "1h"

    for sym in symbols:
        trades = backtest(sym, interval)
        print(trades.head())
