from unittest.mock import patch
from src.executors.trade_manager import place_order

@patch("src.executors.trade_manager.client")
def test_place_order(mock_client):
    mock_client.order_market_buy.return_value = {"status": "FILLED"}
    place_order(1)  # simulate a buy
    mock_client.order_market_buy.assert_called_once()

