import os
from datetime import datetime
from src.db.db_utils import init_db, get_db_session
from src.data.collectors.alpaca_data import fetch_stock_ohlcv
from src.data.collectors.binance_data import fetch_ohlcv as fetch_crypto_ohlcv
from src.ai_models.bitcoin_model import predict as btc_predict
from src.ai_models.stocks_model import predict as stock_predict
from src.executors.crypto_executor import execute_crypto_trade
from src.executors.stock_executor import execute_stock_trade
from src.utils.scheduler import JobScheduler

def trading_job():
    # Crypto BTC
    df_btc = fetch_crypto_ohlcv('BTCUSDT', interval='15m', limit=100)
    sig = btc_predict('BTCUSDT', df_btc)
    print(f"BTC signal: {sig}")
    if sig == 1:
        execute_crypto_trade('BTCUSDT', 'BUY', 0.001)
    elif sig == -1:
        execute_crypto_trade('BTCUSDT', 'SELL', 0.001)

    # Stock AAPL
    df_aapl = fetch_stock_ohlcv('AAPL', timeframe='1D', limit=30)
    sig_s = stock_predict('AAPL', df_aapl)
    print(f"AAPL signal: {sig_s}")
    if sig_s == 'buy':
        execute_stock_trade('AAPL', 1, 'buy')
    elif sig_s == 'sell':
        execute_stock_trade('AAPL', 1, 'sell')
    else:
        print("AAPL hold")

if __name__ == "__main__":
    init_db()
    scheduler = JobScheduler()
    scheduler.add_job(trading_job, every=15, unit='minutes', job_name='Multi-Asset Trading Job')
    scheduler.run_forever()

