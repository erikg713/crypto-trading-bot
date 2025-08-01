# core/trader.py
from exchanges.factory import get_exchange
from strategies.factory import get_strategy
from core.data_streamer import DataStreamer
from core.order_executor import OrderExecutor
from risk.risk_manager import RiskManager

class Trader:
    def __init__(self, exchange_name, strategy_name):
        self.exchange = get_exchange(exchange_name)
        self.strategy = get_strategy(strategy_name)
        self.data_streamer = DataStreamer(self.exchange)
        self.order_executor = OrderExecutor(self.exchange)
        self.risk_manager = RiskManager()

    def run(self):
        for data in self.data_streamer.stream():
            signal = self.strategy.generate_signal(data)
            risk_action = self.risk_manager.evaluate(signal, data)
            if risk_action:
                self.order_executor.execute(risk_action)