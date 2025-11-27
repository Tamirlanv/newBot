from services.coingecko.coingecko_client import CoinGeckoClient
from services.trello.trello_client import TrelloClient
from services.alerts.alert_manager import AlertManager

cg_client = CoinGeckoClient()
trello_client = TrelloClient()

alert_manager = AlertManager(cg_client) 

async def init_all(bot=None):
    await cg_client.init()
    await trello_client.init()

    if bot:
        await alert_manager.start(bot)

async def close_all():
    await cg_client.close()
    await trello_client.close()
