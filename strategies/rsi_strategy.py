# strategies/rsi_strategy.py
from strategies.base_strategy import BaseStrategy
import numpy as np

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