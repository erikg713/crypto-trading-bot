# src/collectors/binance_client.py

import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

def get_binance_client():
    return client

from binance.client import Client
import os
import yaml

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

client = Client(
    api_key=os.getenv("BINANCE_API_KEY", config["binance"]["api_key"]),
    api_secret=os.getenv("BINANCE_SECRET", config["binance"]["api_secret"])
)

