from src.api_clients.binance_client import place_order
from src.db.db_utils import get_db_session
from src.db.models import Trade
from datetime import datetime

def execute_crypto_trade(symbol, side, qty):
    order = place_order(symbol, side, qty)
    if order:
        print(f"Crypto trade executed: {order}")
        # Here you could log trades in DB
        session = get_db_session()
        trade = Trade(symbol=symbol, trade_type=side, price=float(order['fills'][0]['price']), quantity=qty, timestamp=datetime.utcnow())
        session.add(trade)
        session.commit()
        session.close()
        return True
    else:
        print("Crypto trade failed")
        return False

