import logging
import os
from exchanges.binance import BinanceExchange

# ---------------------------
# Setup Logging
# ---------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Trade logger
trade_logger = logging.getLogger("trade_logger")
trade_logger.setLevel(logging.INFO)
trade_handler = logging.FileHandler(os.path.join(LOG_DIR, "trade_log.txt"))
trade_formatter = logging.Formatter('%(asctime)s - %(message)s')
trade_handler.setFormatter(trade_formatter)
trade_logger.addHandler(trade_handler)

# Strategy logger
strategy_logger = logging.getLogger("strategy_logger")
strategy_logger.setLevel(logging.INFO)
strategy_handler = logging.FileHandler(os.path.join(LOG_DIR, "strategy_logs.txt"))
strategy_formatter = logging.Formatter('%(asctime)s - %(message)s')
strategy_handler.setFormatter(strategy_formatter)
strategy_logger.addHandler(strategy_handler)

# ---------------------------
# Order Executor
# ---------------------------
class OrderExecutor:
    def __init__(self, exchange=None):
        self.exchange = exchange or BinanceExchange()

    def execute_trade(self, signal, symbol, amount=1):
        """
        Executes BUY/SELL/HOLD trades and logs the action.
        """
        if signal.upper() == "BUY":
            self.exchange.buy(amount)
            trade_logger.info(f"Executed BUY order: {symbol} {amount}")
        elif signal.upper() == "SELL":
            self.exchange.sell(amount)
            trade_logger.info(f"Executed SELL order: {symbol} {amount}")
        elif signal.upper() == "CLOSE":
            self.exchange.close_position()
            trade_logger.info(f"Closed position: {symbol}")
        else:
            trade_logger.info(f"HOLD signal: {symbol}")
        
        # Log the strategy decision
        strategy_logger.info(f"Signal: {signal} | Symbol: {symbol} | Amount: {amount}")
