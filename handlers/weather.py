from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from services.weather_api import get_weather

router = Router()

@router.message(F.text == "🌤 Погода")
async def kb_weather(message: Message):
    await message.answer("Введите город:\nНапример: погода Париж")

@router.message(F.text.lower().startswith("погода"))
async def weather(message: Message):
    city = message.text.lower().replace("погода", "").strip()
    if not city:
        await message.answer("Введите город: погода <город>")
        return

    result = await get_weather(city)
    await message.answer(result)
