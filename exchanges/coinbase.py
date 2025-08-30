import requests
from datetime import datetime
import hmac
import hashlib
import time
import base64
import json

class CoinbaseExchange:
    """
    Basic Coinbase Pro / Advanced Trade API wrapper for AI-CryptoTrader.
    Supports market data fetching and order execution.
    """

    BASE_URL = "https://api.pro.coinbase.com"  # Use "https://api.exchange.coinbase.com" for live trades

    def __init__(self, api_key: str, api_secret: str, passphrase: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    # ---------------------------
    # Authentication Helper
    # ---------------------------
    def _get_auth_headers(self, method: str, path: str, body: str = "") -> dict:
        timestamp = str(time.time())
        message = timestamp + method.upper() + path + body
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        return {
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-SIGN": signature_b64,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

    # ---------------------------
    # Market Data
    # ---------------------------
    def get_ticker(self, symbol: str) -> dict:
        """
        Get current ticker info for a symbol (e.g., 'ETH-USD').
        """
        path = f"/products/{symbol}/ticker"
        url = self.BASE_URL + path
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error fetching ticker: {response.text}")
        return response.json()

    def get_historical_candles(self, symbol: str, granularity: int = 3600) -> list:
        """
        Fetch historical OHLC candles for a symbol.
        granularity in seconds: 60, 300, 900, 3600, 21600, 86400
        """
        path = f"/products/{symbol}/candles?granularity={granularity}"
        url = self.BASE_URL + path
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error fetching candles: {response.text}")
        return response.json()  # list of [time, low, high, open, close, volume]

    # ---------------------------
    # Order Execution
    # ---------------------------
    def place_order(self, symbol: str, side: str, price: float, size: float, order_type: str = "limit") -> dict:
        """
        Place a buy/sell order.
        side: 'buy' or 'sell'
        order_type: 'limit' or 'market'
        """
        path = "/orders"
        body = {
            "product_id": symbol,
            "side": side.lower(),
            "price": str(price),
            "size": str(size),
            "type": order_type
        }
        body_json = json.dumps(body)
        headers = self._get_auth_headers("POST", path, body_json)
        url = self.BASE_URL + path

        response = requests.post(url, headers=headers, data=body_json)
        if response.status_code not in (200, 201):
            raise Exception(f"Error placing order: {response.text}")
        return response.json()

    # ---------------------------
    # Example Usage
    # ---------------------------
if __name__ == "__main__":
    # Replace with your Coinbase API keys
    API_KEY = "YOUR_KEY"
    API_SECRET = "YOUR_SECRET"
    PASSPHRASE = "YOUR_PASSPHRASE"

    cb = CoinbaseExchange(API_KEY, API_SECRET, PASSPHRASE)

    # Get current ticker
    ticker = cb.get_ticker("ETH-USD")
    print("ETH-USD Ticker:", ticker)

    # Fetch historical candles
    candles = cb.get_historical_candles("ETH-USD", granularity=3600)
    print("Last 5 candles:", candles[:5])
