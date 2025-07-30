import json
import time
import hmac
import hashlib
from websocket import create_connection
from typing import Optional, Dict


class BinanceTrader:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.ws_url = (
            "wss://testnet.binance.vision/ws-api/v3"
            if testnet
            else "wss://ws-api.binance.com:443/ws-api/v3"
        )

    def _sign_params(self, params: dict) -> str:
        query = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _send_request(self, method: str, params: dict, req_id: Optional[str] = None) -> Dict:
        params['apiKey'] = self.api_key
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._sign_params(params)

        request_payload = {
            'id': req_id or f'{method}_{int(time.time())}',
            'method': method,
            'params': params
        }

        ws = create_connection(self.ws_url)
        ws.send(json.dumps(request_payload))
        response = json.loads(ws.recv())
        ws.close()
        return response

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: str,
        price: str,
        time_in_force: str = 'GTC',
        req_id: Optional[str] = None
    ) -> Dict:
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': 'LIMIT',
            'timeInForce': time_in_force,
            'quantity': quantity,
            'price': price
        }
        return self._send_request('order.place', params, req_id)

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: str,
        req_id: Optional[str] = None
    ) -> Dict:
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': 'MARKET',
            'quantity': quantity
        }
        return self._send_request('order.place', params, req_id)