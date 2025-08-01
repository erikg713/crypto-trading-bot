# core/data_streamer.py
import time

class DataStreamer:
    def __init__(self, exchange):
        self.exchange = exchange

    def stream(self):
        while True:
            yield self.exchange.get_market_data()
            time.sleep(1)
