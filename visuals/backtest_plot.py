import matplotlib.pyplot as plt

def plot_rsi_strategy(df, title="RSI Backtest"):
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Price Chart with signals
    axs[0].plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    axs[0].set_title(f"{title} - Price & Signals")
    axs[0].grid(True)

    # Buy/Sell Markers
    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']

    axs[0].scatter(buy_signals['timestamp'], buy_signals['close'], marker='^', color='green', label='Buy Signal', alpha=0.8)
    axs[0].scatter(sell_signals['timestamp'], sell_signals['close'], marker='v', color='red', label='Sell Signal', alpha=0.8)
    axs[0].legend()

    # RSI Chart
    axs[1].plot(df['timestamp'], df['RSI'], label='RSI', color='purple')
    axs[1].axhline(70, linestyle='--', color='red', alpha=0.6)
    axs[1].axhline(30, linestyle='--', color='green', alpha=0.6)
    axs[1].set_title("Relative Strength Index (RSI)")
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()