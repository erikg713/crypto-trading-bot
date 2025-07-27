import os
from src.db.db_utils import init_db, get_db_session
from src.data.collectors.binance_data import fetch_ohlcv
from src.ai_models.bitcoin_model import predict
from src.executors.crypto_executor import execute_crypto_trade
from src.utils.scheduler import JobScheduler

def trading_job():
    print("Fetching BTC data...")
    df = fetch_ohlcv()
    signal = predict(df)
    print(f"Predicted signal: {signal}")

    session = get_db_session()

    last_close = df['close'].iloc[-1]
    trade_qty = 0.001  # example quantity for BTC

    if signal == 1:
        print("Buying BTC...")
        execute_crypto_trade("BTCUSDT", "BUY", trade_qty)
    elif signal == -1:
        print("Selling BTC...")
        execute_crypto_trade("BTCUSDT", "SELL", trade_qty)
    else:
        print("No trade signal")

    session.close()

if __name__ == "__main__":
    init_db()
    scheduler = JobScheduler()
    scheduler.add_job(trading_job, every=15, unit="minutes", job_name="BTC Trading Job")
    scheduler.run_forever()
