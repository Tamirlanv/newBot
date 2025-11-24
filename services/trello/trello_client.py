import aiohttp
import logging
import time

logger = logging.getLogger(__name__)


class CacheTTL:
    def __init__(self, ttl=10):
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


class TrelloError(Exception):
    pass


class TrelloClient:
    
    def __init__(self):
        self.session = None
        self.cache = CacheTTL(ttl=5)
        

    async def init(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()
            

    async def request(self, method, url, params=None):
        if not self.session:
            raise TrelloError("ClientSession not initialized!")

        cache_key = f"{method}:{url}:{tuple(sorted((params or {}).items()))}"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            async with self.session.request(method, url, params=params) as resp:
                if resp.status >= 400:
                    msg = await resp.text()
                    logger.error(f"Trello API error {resp.status}: {msg}")
                    raise TrelloError(msg)

                data = await resp.json()
                self.cache.set(cache_key, data)
                return data

        except Exception as e:
            logger.exception("Trello Request Error")
            raise TrelloError(str(e))


    async def get(self, url, params=None):
        return await self.request("GET", url, params)


    async def post(self, url, params=None):
        return await self.request("POST", url, params)


    async def put(self, url, params=None):
        return await self.request("PUT", url, params)


    async def delete(self, url, params=None):
        return await self.request("DELETE", url, params)
