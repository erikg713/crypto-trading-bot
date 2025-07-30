# traders/binance_trader.py

import json
import time
import hmac
import hashlib
from websocket import create_connection
from typing import Optional

class BinanceTrader:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.ws_url = (
            "wss://testnet.binance.vision/ws-api/v3"
            if testnet else
            "wss://ws-api.binance.com:443/ws-api/v3"
        )

    def _sign_params(self, params: dict) -> str:
        query = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_limit_order(self, symbol: str, side: str, quantity: str, price: str,
                          time_in_force: str = 'GTC', order_id: Optional[str] = None) -> dict:
        timestamp = int(time.time() * 1000)

        params = {
            'apiKey':       self.api_key,
            'symbol':       symbol.upper(),
            'side':         side.upper(),
            'type':         'LIMIT',
            'timeInForce':  time_in_force,
            'quantity':     quantity,
            'price':        price,
            'timestamp':    timestamp
        }
        params['signature'] = self._sign_params(params)

        request_payload = {
            'id': order_id or f'order_{int(time.time())}',
            'method': 'order.place',
            'params': params
        }

        ws = create_connection(self.ws_url)
        ws.send(json.dumps(request_payload))
        response = ws.recv()
        ws.close()

        return json.loads(response)