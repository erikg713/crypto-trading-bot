import unittest
from unittest.mock import patch, MagicMock
from traders.binance_trader import BinanceTrader
import json
import time

class TestBinanceTrader(unittest.TestCase):
    def setUp(self):
        self.api_key = "dummy_key"
        self.api_secret = "dummy_secret"
        self.trader = BinanceTrader(self.api_key, self.api_secret, testnet=True)

    @patch("traders.binance_trader.create_connection")
    def test_place_limit_order(self, mock_create_connection):
        mock_ws = MagicMock()
        mock_response = {"status": "ok", "orderId": 123456}
        mock_ws.recv.return_value = json.dumps(mock_response)
        mock_create_connection.return_value = mock_ws

        response = self.trader.place_limit_order(
            symbol="BTCUSDT",
            side="BUY",
            quantity="0.001",
            price="30000"
        )

        self.assertEqual(response["status"], "ok")
        self.assertIn("orderId", response)
        mock_ws.send.assert_called_once()
        mock_ws.close.assert_called_once()

    @patch("traders.binance_trader.create_connection")
    def test_place_market_order(self, mock_create_connection):
        mock_ws = MagicMock()
        mock_response = {"status": "ok", "orderId": 987654}
        mock_ws.recv.return_value = json.dumps(mock_response)
        mock_create_connection.return_value = mock_ws

        response = self.trader.place_market_order(
            symbol="ETHUSDT",
            side="SELL",
            quantity="0.01"
        )

        self.assertEqual(response["status"], "ok")
        self.assertIn("orderId", response)
        mock_ws.send.assert_called_once()
        mock_ws.close.assert_called_once()

    def test_signature_generation(self):
        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": "0.001",
            "price": "30000",
            "timestamp": int(time.time() * 1000)
        }
        signature = self.trader._sign_params(params)
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 64)

if __name__ == "__main__":
    unittest.main()