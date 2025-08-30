"""
strategies/moving_average.py
============================

Implements simple and exponential moving average (SMA and EMA) strategies
for trading systems or backtesting frameworks.

Features:
- Compute SMA and EMA
- Generate basic buy/sell signals
- Optional integration with Pandas DataFrames for OHLCV data
"""

from typing import List, Optional
import pandas as pd
import pandas as pd
from strategies.base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, df: pd.DataFrame):
        """
        Returns: signal ("BUY", "SELL", "HOLD") and strategy params
        """
        df = df.copy()
        df["short_ma"] = df["close"].rolling(window=self.short_window).mean()
        df["long_ma"] = df["close"].rolling(window=self.long_window).mean()

        signal = "HOLD"
        if df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]:
            signal = "BUY"
        elif df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]:
            signal = "SELL"

        strategy_params = {"short_ma": df["short_ma"].iloc[-1], "long_ma": df["long_ma"].iloc[-1]}
        return signal, strategy_params

def simple_moving_average(prices: List[float], period: int) -> List[float]:
    """
    Calculate the Simple Moving Average (SMA) of a price series.

    Args:
        prices (List[float]): List of prices.
        period (int): Number of periods for the SMA.

    Returns:
        List[float]: SMA values, same length as prices (first `period-1` values are None).
    """
    if period <= 0:
        raise ValueError("Period must be a positive integer")
    
    sma = [None] * (period - 1)
    for i in range(period - 1, len(prices)):
        sma.append(sum(prices[i - period + 1:i + 1]) / period)
    return sma


def exponential_moving_average(prices: List[float], period: int) -> List[float]:
    """
    Calculate the Exponential Moving Average (EMA) of a price series.

    Args:
        prices (List[float]): List of prices.
        period (int): Number of periods for the EMA.

    Returns:
        List[float]: EMA values, same length as prices (first value is initial SMA).
    """
    if period <= 0:
        raise ValueError("Period must be a positive integer")
    ema = []
    k = 2 / (period + 1)
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)  # start with the first price
        else:
            ema.append(price * k + ema[-1] * (1 - k))
    return ema


def generate_signals(prices: List[float], short_period: int = 10, long_period: int = 50) -> List[Optional[str]]:
    """
    Generate trading signals based on SMA crossover strategy.
    
    Buy when short-term SMA crosses above long-term SMA, sell when opposite.

    Args:
        prices (List[float]): Price series.
        short_period (int): Period for short-term SMA.
        long_period (int): Period for long-term SMA.

    Returns:
        List[Optional[str]]: List of signals: 'BUY', 'SELL', or None.
    """
    if short_period >= long_period:
        raise ValueError("Short period must be smaller than long period")

    short_sma = simple_moving_average(prices, short_period)
    long_sma = simple_moving_average(prices, long_period)
    signals = [None]  # First signal cannot be determined

    for i in range(1, len(prices)):
        if short_sma[i] is None or long_sma[i] is None:
            signals.append(None)
        elif short_sma[i] > long_sma[i] and short_sma[i-1] <= long_sma[i-1]:
            signals.append("BUY")
        elif short_sma[i] < long_sma[i] and short_sma[i-1] >= long_sma[i-1]:
            signals.append("SELL")
        else:
            signals.append(None)

    return signals


if __name__ == "__main__":
    # Example usage
    sample_prices = [100, 102, 101, 105, 107, 110, 108, 107, 111, 115, 117]
    print("SMA(3):", simple_moving_average(sample_prices, 3))
    print("EMA(3):", exponential_moving_average(sample_prices, 3))
    print("Signals:", generate_signals(sample_prices, short_period=3, long_period=5))
