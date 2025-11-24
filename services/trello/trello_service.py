from .trello_api import TrelloAPI

class TrelloService:
    def __init__(self, api: TrelloAPI, board_id: str):
        self.api = api
        self.board_id = board_id

    async def list_cards(self):
        return await self.api.get_cards(self.board_id)

    async def list_lists(self):
        return await self.api.get_lists(self.board_id)

    async def create_card(self, name: str, list_id: str):
        return await self.api.create_card(name, list_id)

    async def delete_card(self, card_id: str):
        return await self.api.delete_card(card_id)

    async def update_card(self, card_id: str, name: str):
        return await self.api.update_card(card_id, name)

    async def move_card(self, card_id: str, list_id: str):
        return await self.api.move_card(card_id, list_id)
