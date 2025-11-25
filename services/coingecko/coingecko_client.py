import aiohttp
import time

class CacheTTL:
    def __init__(self, ttl=5):
        self.ttl = ttl
        self.cache = {}

    def get(self, key):
        data = self.cache.get(key)
        if not data:
            return None
        value, ts = data
        if time.time() - ts < self.ttl:
            return value
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())


class CoinGeckoClient:

    BASE = "https://api.coingecko.com/api/v3/"

    def __init__(self):
        self.session = None
        self.cache = CacheTTL(ttl=5)

    async def init(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()

    async def request(self, url, params=None):
        cache_key = f"{url}:{tuple(sorted((params or {}).items()))}"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        async with self.session.get(url, params=params) as resp:
            data = await resp.json()
            if resp.status != 200:
                return {"error": True, "message": str(data)}
            self.cache.set(cache_key, data)
            return data
