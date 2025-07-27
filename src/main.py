import os
from datetime import datetime
from src.db.db_utils import init_db
from src.data.collectors.alpaca_data import fetch_stock_ohlcv
from src.data.collectors.binance_data import fetch_ohlcv as fetch_crypto_ohlcv
from src.ai_models.bitcoin_model import predict as btc_predict
from src.ai_models.stocks_model import predict as stock_predict
from src.executors.crypto_executor import execute_crypto_trade
from src.executors.stock_executor import execute_stock_trade
from src.utils.scheduler import JobScheduler
from src.utils.alerts import notify_telegram

def trading_job():
    try:
        # BTC
        df_btc = fetch_crypto_ohlcv('BTCUSDT', interval='15m', limit=100)
        sig = btc_predict('BTCUSDT', df_btc)
        print(f"BTC signal: {sig}")
        if sig == 1:
            execute_crypto_trade('BTCUSDT', 'BUY', 0.001)
        elif sig == -1:
            execute_crypto_trade('BTCUSDT', 'SELL', 0.001)
        notify_telegram(f"✅ BTC trade signal: {sig} at {datetime.now()}")

        # AAPL
        df_aapl = fetch_stock_ohlcv('AAPL', timeframe='1D', limit=30)
        sig_s = stock_predict('AAPL', df_aapl)
        print(f"AAPL signal: {sig_s}")
        if sig_s == 'buy':
            execute_stock_trade('AAPL', 1, 'buy')
        elif sig_s == 'sell':
            execute_stock_trade('AAPL', 1, 'sell')
        else:
            print("AAPL hold")
        notify_telegram(f"✅ AAPL trade signal: {sig_s} at {datetime.now()}")

    except Exception as e:
        notify_telegram(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    run_bot()

