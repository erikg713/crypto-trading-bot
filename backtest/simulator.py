# backtest/simulator.py
import pandas as pd

class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def load_data(self):
        # Mock data - replace with CSV or API
        return pd.DataFrame({
            "close": [100 + i for i in range(50)]
        })

    def run(self):
        df = self.load_data()
        balance = 1000
        position = None

        for i in range(1, len(df)):
            row = df.iloc[:i+1]
            data = {"close": row["close"]}
            signal = self.strategy.generate_signal(data)

            if signal == "BUY" and position is None:
                entry_price = df.iloc[i]["close"]
                position = entry_price
                print(f"BUY at {entry_price}")

            elif signal == "SELL" and position is not None:
                exit_price = df.iloc[i]["close"]
                pnl = exit_price - position
                balance += pnl
                print(f"SELL at {exit_price} | PnL: {pnl}")
                position = None

        print(f"Final Balance: ${balance:.2f}")