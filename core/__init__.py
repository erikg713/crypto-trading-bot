# core/__init__.py

"""
Core module for AI-CryptoTrader.

Includes:
- Trader engine
- Data streaming
- Order execution
"""

from .trader import Trader
from .data_streamer import DataStreamer
from .order_executor import OrderExecutor

__all__ = [
    "Trader",
    "DataStreamer",
    "OrderExecutor"
]
