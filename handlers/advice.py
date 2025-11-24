from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from services.advice_api import get_advice


router = Router()

@router.message(F.text == "💡 Совет")
async def kb_advice(message: Message):
    await advice(message)

@router.message(Command("advice"))
async def advice(message: Message):
    text = await get_advice()
    await message.answer(f"💡 Совет дня:\n“{text}”")
