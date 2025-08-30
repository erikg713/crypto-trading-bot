import logging
from exchanges import BinanceExchange, CoinbaseExchange

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OrderExecutor:
    """
    Executes buy/sell orders through a specified exchange.
    """

    def __init__(self, exchange, symbol: str):
        """
        exchange: instance of an exchange class (e.g., BinanceExchange, CoinbaseExchange)
        symbol: trading pair (e.g., "ETHUSDT")
        """
        self.exchange = exchange
        self.symbol = symbol

    def execute_order(self, side: str, price: float, size: float, order_type: str = "market"):
        """
        Executes a single order.

        side: "BUY" or "SELL"
        price: order price (ignored for market orders)
        size: order size
        order_type: "market" or "limit"
        """
        side_lower = side.lower()
        logger.info(f"[ORDER] {side_upper(side)} {size} {self.symbol} @ {price} ({order_type})")

        try:
            if isinstance(self.exchange, BinanceExchange):
                order = self.exchange.place_order(symbol=self.symbol, side=side_lower, price=price, size=size, order_type=order_type)
            elif isinstance(self.exchange, CoinbaseExchange):
                order = self.exchange.place_order(symbol=self.symbol, side=side_lower, price=price, size=size, order_type=order_type)
            else:
                raise ValueError("Unsupported exchange type")
            
            logger.info(f"[ORDER EXECUTED] {order}")
            return order

        except Exception as e:
            logger.error(f"[ERROR] Failed to execute order: {e}")
            return None

def side_upper(side: str):
    """Helper to normalize side string for logging"""
    return side.upper()

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    # Example using Coinbase
    from exchanges.coinbase import CoinbaseExchange
    API_KEY = "YOUR_KEY"
    API_SECRET = "YOUR_SECRET"
    PASSPHRASE = "YOUR_PASSPHRASE"

    coinbase = CoinbaseExchange(API_KEY, API_SECRET, PASSPHRASE)
    executor = OrderExecutor(coinbase, "ETH-USD")

    # Execute a test market buy order
    executor.execute_order("BUY", price=0, size=0.01, order_type="market")
