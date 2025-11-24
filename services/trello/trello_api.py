import logging
from .trello_client import TrelloClient, TrelloError

logger = logging.getLogger(__name__)


class TrelloAPI:
    
    BASE = "https://api.trello.com/1"

    def __init__(self, key: str, token: str, client: TrelloClient):
        self.key = key
        self.token = token
        self.client = client
        

    def _auth(self):
        return {"key": self.key, "token": self.token}
    

    async def safe(self, coro):
        try:
            return await coro
        except TrelloError as e:
            return {"error": True, "message": str(e)}
        except Exception as e:
            return {"error": True, "message": "Unexpected error", "details": str(e)}
        

    async def get_lists(self, board_id):
        return await self.safe(
            self.client.get(f"{self.BASE}/boards/{board_id}/lists", self._auth())
        )
        

    async def get_cards(self, board_id):
        return await self.safe(
            self.client.get(f"{self.BASE}/boards/{board_id}/cards", self._auth())
        )
        

    async def create_card(self, name, list_id):
        params = {"name": name, "idList": list_id, **self._auth()}
        return await self.safe(self.client.post(f"{self.BASE}/cards", params))
    

    async def delete_card(self, card_id):
        return await self.safe(
            self.client.delete(f"{self.BASE}/cards/{card_id}", self._auth())
        )
        

    async def update_card(self, card_id, name):
        params = {"name": name, **self._auth()}
        return await self.safe(
            self.client.put(f"{self.BASE}/cards/{card_id}", params)
        )
        

    async def move_card(self, card_id, list_id):
        params = {"idList": list_id, **self._auth()}
        return await self.safe(
            self.client.put(f"{self.BASE}/cards/{card_id}", params)
        )
