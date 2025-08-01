# exchanges/factory.py
def get_exchange(name):
    if name == "binance":
        from exchanges.binance import BinanceExchange
        return BinanceExchange()
    elif name == "alpaca":
        from exchanges.alpaca import AlpacaExchange
        return AlpacaExchange()
    else:
        raise ValueError("Unsupported exchange")