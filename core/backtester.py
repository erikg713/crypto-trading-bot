import pandas as pd
from core.order_executor import OrderExecutor
from strategies.base_strategy import BaseStrategy
from datetime import datetime

class Backtester:
    """
    Backtesting engine for crypto trading strategies.
    Simulates trades over historical OHLCV data.
    """

    def __init__(self, symbol="BTCUSDT", strategy: BaseStrategy = None, amount=1, historical_csv=None):
        self.symbol = symbol
        self.strategy = strategy or BaseStrategy()
        self.amount = amount
        self.executor = OrderExecutor(exchange=None)  # No live exchange
        self.historical_csv = historical_csv or f"data/raw/market/{symbol}.csv"
        self.data = pd.read_csv(self.historical_csv, parse_dates=["timestamp"])
        self.results = []

    def run(self):
        """
        Run the backtest over historical data.
        """
        print(f"[INFO] Starting backtest for {self.symbol} using {self.strategy.__class__.__name__}")
        for index in range(len(self.data)):
            row = self.data.iloc[:index+1]  # Pass all historical data up to current point
            signal, strategy_params = self.strategy.generate_signal(row)
            
            # Execute trade simulation (logs PnL internally)
            self.executor.execute_trade(signal, self.symbol, amount=self.amount, strategy_params=strategy_params)
            
            # Record result for analytics
            current_price = row["close"].iloc[-1]
            position = self.executor.positions.get(self.symbol)
            pnl = 0
            if position:
                pnl = (current_price - position["price"]) * position["amount"]
            self.results.append({
                "timestamp": row["timestamp"].iloc[-1],
                "signal": signal,
                "price": current_price,
                "pnl": pnl
            })

        print("[INFO] Backtest completed.")
        return pd.DataFrame(self.results)

if __name__ == "__main__":
    from strategies.moving_average import MovingAverageStrategy

    strategy = MovingAverageStrategy(short_window=5, long_window=20)
    backtester = Backtester(symbol="BTCUSDT", strategy=strategy, amount=0.01)
    results_df = backtester.run()
    print(results_df.head())
    results_df.to_csv("logs/backtest_results.csv", index=False)
