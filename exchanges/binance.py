# exchanges/binance.py
from exchanges.base_exchange import BaseExchange

class BinanceExchange(BaseExchange):
    def get_market_data(self):
        return {"close": 300.0}  # Replace with Binance API call

    def buy(self):
        print("Binance BUY")

    def sell(self):
        print("Binance SELL")

    def close_position(self):
        print("Binance CLOSE")