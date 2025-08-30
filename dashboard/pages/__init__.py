"""
Pages package for AI-CryptoTrader Dash app.

Modules:
- overview     : Main charts and portfolio summary
- trades       : Detailed trade table & analytics
- strategy     : Controls for strategy parameters
- performance  : Equity curves, drawdown, Sharpe ratio
"""

from .overview import overview_layout
from .trades import trades_layout
from .strategy import strategy_layout
from .performance import performance_layout
