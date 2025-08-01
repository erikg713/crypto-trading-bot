# utils/visualize.py
import matplotlib.pyplot as plt

def plot_signals(df, signals):
    buy_signals = df[signals == 'BUY']
    sell_signals = df[signals == 'SELL']

    plt.figure(figsize=(14, 7))
    plt.plot(df['close'], label='Price', alpha=0.7)
    plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', label='Buy', alpha=1.0)
    plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', label='Sell', alpha=1.0)
    plt.title("RSI-AI Hybrid Strategy Trades")
    plt.legend()
    plt.grid(True)
    plt.show()