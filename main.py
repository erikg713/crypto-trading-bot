📁 ai_crypto_trader/

main.py

import argparse from core.trader import Trader

if name == "main": parser = argparse.ArgumentParser() parser.add_argument("--exchange", type=str, required=True) parser.add_argument("--strategy", type=str, required=True) args = parser.parse_args()

trader = Trader(exchange_name=args.exchange, strategy_name=args.strategy)
trader.run()

core/trader.py

from exchanges.factory import get_exchange from strategies.factory import get_strategy from core.data_streamer import DataStreamer from core.order_executor import OrderExecutor from risk.risk_manager import RiskManager

class Trader: def init(self, exchange_name, strategy_name): self.exchange = get_exchange(exchange_name) self.strategy = get_strategy(strategy_name) self.data_streamer = DataStreamer(self.exchange) self.order_executor = OrderExecutor(self.exchange) self.risk_manager = RiskManager()

def run(self):
    for data in self.data_streamer.stream():
        signal = self.strategy.generate_signal(data)
        risk_action = self.risk_manager.evaluate(signal, data)
        if risk_action:
            self.order_executor.execute(risk_action)

core/data_streamer.py

import time

class DataStreamer: def init(self, exchange): self.exchange = exchange

def stream(self):
    while True:
        yield self.exchange.get_market_data()
        time.sleep(1)

core/order_executor.py

class OrderExecutor: def init(self, exchange): self.exchange = exchange

def execute(self, action):
    if action == "BUY":
        self.exchange.buy()
    elif action == "SELL":
        self.exchange.sell()
    elif action == "CLOSE":
        self.exchange.close_position()

exchanges/factory.py

def get_exchange(name): if name == "binance": from exchanges.binance import BinanceExchange return BinanceExchange() elif name == "alpaca": from exchanges.alpaca import AlpacaExchange return AlpacaExchange() else: raise ValueError("Unsupported exchange")

exchanges/base_exchange.py

class BaseExchange: def get_market_data(self): raise NotImplementedError

def buy(self):
    raise NotImplementedError

def sell(self):
    raise NotImplementedError

def close_position(self):
    raise NotImplementedError

exchanges/binance.py

from exchanges.base_exchange import BaseExchange

class BinanceExchange(BaseExchange): def get_market_data(self): return {"close": 300.0}  # Replace with Binance API call

def buy(self):
    print("Binance BUY")

def sell(self):
    print("Binance SELL")

def close_position(self):
    print("Binance CLOSE")

exchanges/alpaca.py

from exchanges.base_exchange import BaseExchange

class AlpacaExchange(BaseExchange): def get_market_data(self): return {"close": 100.0}  # Replace with Alpaca API call

def buy(self):
    print("Alpaca BUY")

def sell(self):
    print("Alpaca SELL")

def close_position(self):
    print("Alpaca CLOSE")

