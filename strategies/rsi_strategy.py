# strategies/rsi_strategy.py
from strategies.base_strategy import BaseStrategy
import numpy as np
import pandas as pd

class RSIStrategy:
    def __init__(self, rsi_period=14, lower_thresh=30, upper_thresh=70):
        self.rsi_period = rsi_period
        self.lower_thresh = lower_thresh
        self.upper_thresh = upper_thresh

    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['RSI'] = self.calculate_rsi(df['close'])

        df['signal'] = 'HOLD'
        df.loc[df['RSI'] < self.lower_thresh, 'signal'] = 'BUY'
        df.loc[df['RSI'] > self.upper_thresh, 'signal'] = 'SELL'

        return df
class RSIStrategy(BaseStrategy):
    def generate_signal(self, data):
        close = np.array(data["close"])
        delta = np.diff(close)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = np.mean(gain[-14:])
        avg_loss = np.mean(loss[-14:])

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        if rsi > 70:
            return "SELL"
        elif rsi < 30:
            return "BUY"
        else:
            return "HOLD"