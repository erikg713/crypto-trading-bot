# mnt/data/src/data/__init__.py
"""
Data package for AI-CryptoTrader.

This package handles:
- Loading raw market data from CSV files
- Preprocessing and feature engineering
- Trade history management
- Utility functions for backtesting and analysis

Modules:
- loader.py       : Load OHLCV data for symbols (ETHUSDT, SOLUSDT, etc.)
- preprocess.py   : Add features like SMA, RSI, returns
- trades.py       : Save/load trades for backtesting
- utils.py        : Helper functions (train/test split, etc.)
"""
