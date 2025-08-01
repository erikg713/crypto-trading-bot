import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from strategies.base_strategy import BaseStrategy

class HybridRSIAIStrategy(BaseStrategy):
    def __init__(self, rsi_period=14, trend_window=10):
        self.rsi_period = rsi_period
        self.trend_window = trend_window

    def compute_rsi(self, prices):
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(self.rsi_period).mean()
        avg_loss = loss.rolling(self.rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-6)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def predict_trend(self, prices):
        if len(prices) < self.trend_window:
            return 0

        y = prices[-self.trend_window:].values.reshape(-1, 1)
        x = np.arange(len(y)).reshape(-1, 1)

        model = LinearRegression().fit(x, y)
        return model.coef_[0][0]

    def generate_signal(self, df):
        if len(df) < self.rsi_period + self.trend_window:
            return 'HOLD'

        rsi_series = self.compute_rsi(df['close'])
        current_rsi = rsi_series.iloc[-1]
        trend = self.predict_trend(df['close'])

        if current_rsi < 30 and trend > 0:
            return 'BUY'
        elif current_rsi > 70 and trend < 0:
            return 'SELL'
        else:
            return 'HOLD'