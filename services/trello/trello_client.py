from services.http_client import HTTPClient

class TrelloClient(HTTPClient):
    def __init__(self):
        super().__init__("https://api.trello.com/1")
