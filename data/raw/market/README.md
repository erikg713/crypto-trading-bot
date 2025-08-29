# Market Data (Raw)

This folder stores raw OHLCV market data for backtesting and training.

- **BTCUSDT.csv** → Bitcoin to USDT trading pair.
- **ETHUSDT.csv** → Ethereum to USDT trading pair.
- **SOLUSDT.csv** → Solana to USDT trading pair.
- **market_metadata.json** → Metadata about the exchange, pairs, and granularity.

⚠️ Do not modify raw files directly. Use preprocessing scripts in `scripts/` to clean and prepare data.
