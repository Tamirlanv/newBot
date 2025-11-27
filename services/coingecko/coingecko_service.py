from .coingecko_api import CoinGeckoAPI

class CryptoAlert:
    def __init__(self, user_id, coin, target, direction, currency="usd", alert_id=None):
        self.id = alert_id
        self.user_id = user_id
        self.coin = coin
        self.target = target
        self.direction = direction
        self.currency = currency

class CoinGeckoService:
    def __init__(self, api: CoinGeckoAPI):
        self.api = api

    async def get_price(self, coin, currency="usd"):
        return await self.api.get_price(coin, currency)

    async def convert(self, amount, coin, currency="usd"):
        return await self.api.convert(amount, coin, currency)

    async def get_coin_list(self):
        return await self.api.get_coin_list()

    async def get_trending(self):
        return await self.api.get_trending()

    async def get_top(self, vs_currency="usd", per_page=10, page=1):
        return await self.api.get_markets(vs_currency, per_page, page)

    async def get_coin(self, coin_id):
        return await self.api.get_coin(coin_id)

    async def get_chart(self, coin, currency="usd", days=7):
        return await self.api.get_chart(coin, currency, days)
