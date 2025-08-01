import matplotlib.pyplot as plt
import pandas as pd
from strategies.hybrid_strategy import HybridStrategy

class VisualBacktester:
    def __init__(self, price_data: pd.Series):
        self.prices = price_data
        self.strategy = HybridStrategy()
        self.signals = []

    def run(self):
        # Train AI on first 100 data points (demo purpose)
        train_prices = self.prices[:100]
        labels = [1 if train_prices[i+1] > train_prices[i] else 0 for i in range(len(train_prices) - 1)]
        self.strategy.train_ai(train_prices[:-1], labels)

        # Generate signals for remaining prices
        for i in range(100, len(self.prices)):
            window = self.prices[i-15:i].tolist()
            signal = self.strategy.generate_signal(window)
            self.signals.append(signal)

    def plot(self):
        price_plot = self.prices[100:].reset_index(drop=True)
        signals = pd.Series(self.signals)

        plt.figure(figsize=(14, 6))
        plt.plot(price_plot, label="Price", color='lightgray')

        # Plot buy signals
        buy_points = price_plot[signals == 'BUY']
        sell_points = price_plot[signals == 'SELL']

        plt.scatter(buy_points.index, buy_points, color='green', label='BUY', marker='^', s=100)
        plt.scatter(sell_points.index, sell_points, color='red', label='SELL', marker='v', s=100)

        plt.title("Hybrid Strategy Visual Backtest")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()