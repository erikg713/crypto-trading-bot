"""
Exchanges package for AI-CryptoTrader.

This package contains exchange connectors for multiple platforms:
- Binance
- Coinbase
- Alpaca (future)
- Others (plug-in architecture)

You can import exchanges like:

from exchanges import BinanceExchange, CoinbaseExchange
"""

from .binance import BinanceExchange
from .coinbase import CoinbaseExchange

# Optional: add other exchange imports here in the future
# from .alpaca import AlpacaExchange
