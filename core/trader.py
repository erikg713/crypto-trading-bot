import time
import pandas as pd
from core.order_executor import OrderExecutor
from strategies.base_strategy import BaseStrategy
from exchanges.binance import BinanceExchange
from exchanges.coinbase import CoinbaseExchange  # Optional: other exchanges

class Trader:
    """
    Main trading engine.
    Executes signals from strategies on a chosen exchange.
    """

    def __init__(self, exchange_name="binance", strategy: BaseStrategy = None, symbol="BTCUSDT", amount=1):
        # Initialize exchange wrapper
        if exchange_name.lower() == "binance":
            self.exchange = BinanceExchange()
        elif exchange_name.lower() == "coinbase":
            self.exchange = CoinbaseExchange()
        else:
            raise ValueError(f"Unknown exchange: {exchange_name}")

        self.symbol = symbol
        self.amount = amount
        self.strategy = strategy or BaseStrategy()
        self.executor = OrderExecutor(exchange=self.exchange)

    def fetch_market_data(self) -> pd.DataFrame:
        """
        Fetch historical market data for strategy calculation.
        Can be extended to real-time streaming.
        """
        df = pd.read_csv(f"data/raw/market/{self.symbol}.csv", parse_dates=["timestamp"])
        return df

    def run(self, interval=60):
        """
        Run the trading loop.
        interval: loop interval in seconds (default 60s)
        """
        print(f"[INFO] Starting trading bot for {self.symbol} on {self.exchange.__class__.__name__}...")
        try:
            while True:
                # Fetch market data
                data = self.fetch_market_data()

                # Generate strategy signal
                signal, strategy_params = self.strategy.generate_signal(data)

                # Execute trade
                self.executor.execute_trade(signal, self.symbol, amount=self.amount, strategy_params=strategy_params)

                # Wait until next interval
                time.sleep(interval)

        except KeyboardInterrupt:
            print("[INFO] Trading bot stopped manually.")
        except Exception as e:
            print(f"[ERROR] Trader encountered an error: {e}")
