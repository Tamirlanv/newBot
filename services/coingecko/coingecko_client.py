# services/coingecko/coingecko_client.py
from services.http_client import HTTPClient

class CoinGeckoClient(HTTPClient):

    def __init__(self):
        super().__init__("https://api.coingecko.com/api/v3")
