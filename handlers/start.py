from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.keyboards import main_kb

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я многофункциональный бот 😊\n\n"
        "Доступные команды:\n"
        "/about — о боте\n"
        "Используй кнопки ниже 👇",
        reply_markup=main_kb
    )

@router.message(Command("about"))
async def about(message: Message):
    await message.answer("🤖 Я бот, который показывает погоду, советы и конвертирует валюты!")

