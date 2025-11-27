from services.coingecko.coingecko_client import CoinGeckoClient

class CoinGeckoAPI:

    def __init__(self, api_key: str, client: CoinGeckoClient):
        self.api_key = api_key
        self.client = client

    def auth(self):
        return {"x_cg_demo_api_key": self.api_key}

    async def price(self, coin, vs):

        params = {
            "ids": coin,
            "vs_currencies": vs,
            **self.auth()
        }

        return await self.client.get("/simple/price", params)

    async def list_coins(self):
        return await self.client.get("/coins/list", self.auth())
