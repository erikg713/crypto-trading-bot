import pandas as pd
import time
from exchanges.binance import BinanceExchange
from exchanges.coinbase import CoinbaseExchange  # Optional: other exchanges

class DataStreamer:
    """
    Streams market data for a given symbol from a specified exchange.
    Can stream historical CSV data or real-time price data.
    """

    def __init__(self, exchange_name="binance", symbol="BTCUSDT", interval=60):
        self.symbol = symbol
        self.interval = interval  # Interval in seconds
        if exchange_name.lower() == "binance":
            self.exchange = BinanceExchange()
        elif exchange_name.lower() == "coinbase":
            self.exchange = CoinbaseExchange()
        else:
            raise ValueError(f"Unknown exchange: {exchange_name}")

    def stream_historical(self, start_index=0):
        """
        Generator for streaming historical CSV data row by row.
        Useful for backtesting.
        """
        df = pd.read_csv(f"data/raw/market/{self.symbol}.csv", parse_dates=["timestamp"])
        for i in range(start_index, len(df)):
            yield df.iloc[i]
            time.sleep(self.interval)

    def stream_realtime(self):
        """
        Generator for streaming real-time market prices.
        """
        while True:
            data = self.exchange.get_market_data()
            yield data
            time.sleep(self.interval)

if __name__ == "__main__":
    # Example usage: streaming historical BTCUSDT
    streamer = DataStreamer(exchange_name="binance", symbol="BTCUSDT", interval=1)
    for row in streamer.stream_historical(start_index=0):
        print(row)
        break  # Remove break to stream all rows

    # Example usage: streaming real-time price
    # for data in streamer.stream_realtime():
    #     print(data)
