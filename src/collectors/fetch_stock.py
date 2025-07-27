import pandas as pd
import yfinance as yf

def fetch_stock(symbol="AAPL", period="1d", interval="5m"):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    df = df[["Open","High","Low","Close","Volume"]]
    df.columns = ["open","high","low","close","volume"]
    return df
