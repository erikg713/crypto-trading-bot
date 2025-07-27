import os
import alpaca_trade_api as tradeapi
import pandas as pd

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version='v2')

def fetch_stock_ohlcv(symbol: str, timeframe: str = '1D', limit: int = 100):
    barset = api.get_barset(symbol, timeframe, limit=limit)
    bars = barset[symbol]
    data = [{
        'time': b.t.isoformat(),
        'open': b.o,
        'high': b.h,
        'low': b.l,
        'close': b.c,
        'volume': b.v
    } for b in bars]
    return pd.DataFrame(data).set_index('time').astype(float)

# Options data requires separate provider; stub for future.
