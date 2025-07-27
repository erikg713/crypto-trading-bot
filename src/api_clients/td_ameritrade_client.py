# src/api_clients/td_ameritrade_client.py

import requests
import os

API_KEY = os.getenv("TD_AMERITRADE_API_KEY")
BASE_URL = "https://api.tdameritrade.com/v1"

def get_quotes(symbol):
    if not API_KEY:
        raise ValueError("TD Ameritrade API key missing in environment variables")
    endpoint = f"{BASE_URL}/marketdata/{symbol}/quotes"
    params = {"apikey": API_KEY}
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

