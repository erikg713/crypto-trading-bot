# src/main.py
import os
import time
import yaml
from src.learners.predict_signals import get_latest_signal
from src.executors.trade_manager import place_order
from src.executors.risk_controls import validate_risk
from src.collectors.binance_client import get_binance_client
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

# Load settings
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

INTERVAL_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
}

SYMBOL = config["trade"]["symbol"]
QUANTITY = config["trade"]["quantity"]
THRESHOLD = config["trade"]["confidence_threshold"]
INTERVAL = config["trade"]["interval"]
SLEEP_TIME = INTERVAL_SECONDS.get(INTERVAL, 900)

def get_available_usdt():
    client = get_binance_client()
    balance = client.get_asset_balance(asset="USDT")
    return float(balance["free"])

def run_bot():
    print("🚀 AI Crypto Trading Bot is running...")

    while True:
        try:
            signal, confidence = get_latest_signal()
            print(f"Signal: {signal} | Confidence: {confidence:.2f}")

            if signal == 1 and confidence >= THRESHOLD:
                usdt = get_available_usdt()
                approx_cost = QUANTITY * 20000  # Adjust based on BTC price
                if validate_risk(usdt, approx_cost):
                    place_order(signal)
                else:
                    print("🛑 Trade rejected by risk control.")
            else:
                print("⏸️ No trade — Holding position.")

        except Exception as e:
            print(f"❌ ERROR: {e}")

        print(f"⏳ Sleeping for {SLEEP_TIME // 60} minutes...\n")
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    run_bot()

