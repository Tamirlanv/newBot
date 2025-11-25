import aiohttp
import time
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class CacheTTL:
    
    def __init__(self, ttl: int = 10):
        
        self.ttl = ttl
        self.cache: Dict[str, tuple] = {}
        

    def get(self, key: str) -> Optional[dict]:
        
        data = self.cache.get(key)
        if not data:
            return None
        value, ts = data
        if time.time() - ts < self.ttl:
            return value
        return None
    

    def set(self, key: str, value: dict):
        
        self.cache[key] = (value, time.time())




class HTTPClient:
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache = CacheTTL(ttl=5)
        

    async def init(self):
        
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, url: str, params: Optional[dict] = None) -> Optional[dict]:
        
        if self.session is None:
            raise ValueError("Клиентская сессия не инициализирована!")

        cache_key = f"{method}:{url}:{tuple(sorted((params or {}).items()))}"

        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            async with self.session.request(method, self.base_url + url, params=params) as resp:
                if resp.status >= 400:
                    msg = await resp.text()
                    logger.error(f"ошибка API {resp.status}: {msg}")
                    raise Exception(msg)

                data = await resp.json()
                self.cache.set(cache_key, data)
                return data

        except Exception as e:
            logger.exception("Ошибка запроса")
            raise Exception(f"Ошибка в запросе: {str(e)}")


    async def get(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        return await self._request("GET", url, params)

    async def post(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        return await self._request("POST", url, params)

    async def put(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        return await self._request("PUT", url, params)

    async def delete(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        return await self._request("DELETE", url, params)
