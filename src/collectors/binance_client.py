from binance.client import Client
import os
import yaml

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

client = Client(
    api_key=os.getenv("BINANCE_API_KEY", config["binance"]["api_key"]),
    api_secret=os.getenv("BINANCE_SECRET", config["binance"]["api_secret"])
)

