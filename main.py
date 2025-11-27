import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from database import init_db
from handlers import global_router  
import logging
from services.instances import *
from services.alerts.alert_manager import set_alert_manager


logging.basicConfig(
    level=logging.DEBUG,   
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

load_dotenv()

bot = Bot(os.getenv("TELEGRAM_API_KEY"))
dp = Dispatcher()
dp.include_router(global_router)



logging.getLogger("aiogram").setLevel(logging.INFO)
logging.getLogger("aiohttp").setLevel(logging.INFO)

async def main():
    await cg_client.init()
    await trello_client.init()
    set_alert_manager(alert_manager)
    await alert_manager.start(bot)
    init_db()
    try:
        await dp.start_polling(bot)
    finally:
        await cg_client.close()
        await trello_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exist")
