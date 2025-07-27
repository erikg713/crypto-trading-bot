from src.api_clients.alpaca_client import place_order
from src.db.db_utils import get_db_session
from src.db.models import Trade
from datetime import datetime

def execute_stock_trade(symbol, qty, side):
    order = place_order(symbol, qty, side)
    if order:
        print(f"Stock trade executed: {order}")
        session = get_db_session()
        trade = Trade(symbol=symbol, trade_type=side, price=float(order.filled_avg_price or 0), quantity=qty, timestamp=datetime.utcnow())
        session.add(trade)
        session.commit()
        session.close()
        return True
    else:
        print("Stock trade failed")
        return False

