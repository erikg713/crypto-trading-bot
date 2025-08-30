"""
Reusable Dash components for AI-CryptoTrader dashboard.

Modules:
- trade_table       : Show executed trades
- portfolio_summary : Show portfolio statistics and PnL
- strategy_controls : User inputs for strategy parameters
"""
from .trade_table import trade_table_component
from .portfolio_summary import portfolio_summary_component
from .strategy_controls import strategy_controls_component
