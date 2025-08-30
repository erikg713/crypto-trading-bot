import logging
import os
from exchanges.binance import BinanceExchange

# ---------------------------
# Setup Logging
# ---------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Trade logger (includes PnL and price)
trade_logger = logging.getLogger("trade_logger")
trade_logger.setLevel(logging.INFO)
trade_handler = logging.FileHandler(os.path.join(LOG_DIR, "trade_log.txt"))
trade_formatter = logging.Formatter('%(asctime)s - %(message)s')
trade_handler.setFormatter(trade_formatter)
trade_logger.addHandler(trade_handler)

# Strategy logger (records strategy params and signals)
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
        self.positions = {}  # Track open positions: {symbol: {'price': float, 'amount': float}}

    def execute_trade(self, signal, symbol, amount=1, strategy_params=None):
        """
        Executes BUY/SELL/HOLD trades, logs trade + PnL + strategy params.
        """
        current_price = self.exchange.get_market_data()["close"]
        strategy_params = strategy_params or {}

        # Track positions
        if signal.upper() == "BUY":
            self.positions[symbol] = {"price": current_price, "amount": amount}
            self.exchange.buy(amount)
            trade_logger.info(f"BUY {symbol} | Amount: {amount} | Price: {current_price:.2f} | Strategy: {strategy_params}")
        elif signal.upper() == "SELL":
            if symbol in self.positions:
                entry_price = self.positions[symbol]["price"]
                pnl = (current_price - entry_price) * self.positions[symbol]["amount"]
                trade_logger.info(f"SELL {symbol} | Amount: {amount} | Price: {current_price:.2f} | PnL: {pnl:.2f} | Strategy: {strategy_params}")
                del self.positions[symbol]
            self.exchange.sell(amount)
        elif signal.upper() == "CLOSE":
            if symbol in self.positions:
                entry_price = self.positions[symbol]["price"]
                pnl = (current_price - entry_price) * self.positions[symbol]["amount"]
                trade_logger.info(f"CLOSE {symbol} | Price: {current_price:.2f} | PnL: {pnl:.2f} | Strategy: {strategy_params}")
                del self.positions[symbol]
            self.exchange.close_position()
        else:
            trade_logger.info(f"HOLD {symbol} | Price: {current_price:.2f} | Strategy: {strategy_params}")

        # Always log strategy decision
        strategy_logger.info(f"Signal: {signal} | Symbol: {symbol} | Price: {current_price:.2f} | Params: {strategy_params} | Positions: {self.positions}")
