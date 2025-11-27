from services.trello.trello_client import TrelloClient
class TrelloAPI:

    def __init__(self, key: str, token: str, client: TrelloClient):
        self.key = key
        self.token = token
        self.client = client

    def auth(self):
        return {"key": self.key, "token": self.token}

    async def get_lists(self, board_id):
        return await self.client.get(f"/boards/{board_id}/lists", self.auth())

    async def get_cards(self, board_id):
        return await self.client.get(f"/boards/{board_id}/cards", self.auth())

    async def create_card(self, name, list_id):
        params = {"name": name, "idList": list_id, **self.auth()}
        return await self.client.post("/cards", params)

    async def delete_card(self, card_id):
        return await self.client.delete(f"/cards/{card_id}", self.auth())

    async def update_card(self, card_id, name):
        params = {"name": name, **self.auth()}
        return await self.client.put(f"/cards/{card_id}", params)

    async def move_card(self, card_id, list_id):
        params = {"idList": list_id, **self.auth()}
        return await self.client.put(f"/cards/{card_id}", params)
