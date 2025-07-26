# stream_live.py
def stream():
    while True:
        df = fetch_ohlcv("BTCUSDT", "1m", limit=30)
        signal, confidence = predict(df)
        if confidence > 0.8:
            signal_queue.put((signal, confidence))
