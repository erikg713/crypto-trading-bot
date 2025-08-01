# core/trader.py
from exchanges.factory import get_exchange
from strategies.factory import get_strategy
from core.data_streamer import DataStreamer
from core.order_executor import OrderExecutor
from risk.risk_manager import RiskManager
from backtest.simulator import Backtester

class Trader:
    def __init__(self, exchange_name, strategy_name, backtest=False):
        self.exchange = get_exchange(exchange_name)
        self.strategy = get_strategy(strategy_name)
        self.backtest = backtest
        self.risk_manager = RiskManager()
        if not backtest:
            self.data_streamer = DataStreamer(self.exchange)
            self.order_executor = OrderExecutor(self.exchange)

    def run(self):
        if self.backtest:
            backtester = Backtester(self.strategy)
            backtester.run()
        else:
            for data in self.data_streamer.stream():
                signal = self.strategy.generate_signal(data)
                risk_action = self.risk_manager.evaluate(signal, data)
                if risk_action:
                    self.order_executor.execute(risk_action)