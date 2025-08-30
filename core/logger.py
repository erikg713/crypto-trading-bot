import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Trade logger
trade_logger = logging.getLogger("trade_logger")
trade_logger.setLevel(logging.INFO)
trade_handler = logging.FileHandler(os.path.join(LOG_DIR, "trade_log.txt"))
trade_formatter = logging.Formatter('%(asctime)s - %(message)s')
trade_handler.setFormatter(trade_formatter)
trade_logger.addHandler(trade_handler)

# System logger
system_logger = logging.getLogger("system_logger")
system_logger.setLevel(logging.INFO)
system_handler = logging.FileHandler(os.path.join(LOG_DIR, "system_logs.txt"))
system_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
system_handler.setFormatter(system_formatter)
system_logger.addHandler(system_handler)

# Strategy logger
strategy_logger = logging.getLogger("strategy_logger")
strategy_logger.setLevel(logging.INFO)
strategy_handler = logging.FileHandler(os.path.join(LOG_DIR, "strategy_logs.txt"))
strategy_formatter = logging.Formatter('%(asctime)s - %(message)s')
strategy_handler.setFormatter(strategy_formatter)
strategy_logger.addHandler(strategy_handler)

# Example usage
if __name__ == "__main__":
    trade_logger.info("Executed BUY order: BTCUSDT 0.01 at 30000")
    system_logger.warning("API connection unstable")
    strategy_logger.info("RSI signal: BUY for ETHUSDT")
