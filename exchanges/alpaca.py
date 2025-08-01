# exchanges/alpaca.py
from exchanges.base_exchange import BaseExchange

class AlpacaExchange(BaseExchange):
    def get_market_data(self):
        return {"close": 100.0}  # Replace with Alpaca API call

    def buy(self):
        print("Alpaca BUY")

    def sell(self):
        print("Alpaca SELL")

    def close_position(self):
        print("Alpaca CLOSE")
