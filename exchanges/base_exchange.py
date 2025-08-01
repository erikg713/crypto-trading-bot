# exchanges/base_exchange.py
class BaseExchange:
    def get_market_data(self):
        raise NotImplementedError

    def buy(self):
        raise NotImplementedError

    def sell(self):
        raise NotImplementedError

    def close_position(self):
        raise NotImplementedError