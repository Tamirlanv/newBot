from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import save_cg_key, get_cg_key
from services.coingecko.coingecko_client import CoinGeckoClient
from services.coingecko.coingecko_api import CoinGeckoAPI

router = Router()

cg_client = CoinGeckoClient()


class CGAuth(StatesGroup):
    waiting_key = State()


@router.message(F.text == "💰 CoinGecko")
async def cg_start(message: Message, state: FSMContext):
    key = get_cg_key(message.from_user.id)

    if key:
        return await message.answer("✔ API key уже сохранён! Можно работать.")

    await message.answer("Введите ваш CoinGecko Demo API Key:")
    await state.set_state(CGAuth.waiting_key)


@router.message(CGAuth.waiting_key)
async def cg_got_key(message: Message, state: FSMContext):
    save_cg_key(message.from_user.id, message.text)
    await message.answer("🔑 Ключ сохранён!")
    await state.clear()

@router.message(F.text.startswith("/price"))
async def cg_price(message: Message):
    args = message.text.split()

    if len(args) != 3:
        return await message.answer("Формат: /price bitcoin usd")

    coin, vs = args[1], args[2]
    api_key = get_cg_key(message.from_user.id)

    if not api_key:
        return await message.answer("Сначала введите CoinGecko API Key!")

    api = CoinGeckoAPI(api_key, cg_client)
    await cg_client.init()

    data = await api.price(coin, vs)

    if "error" in data:
        return await message.answer("Ошибка API!")

    price = data.get(coin, {}).get(vs)
    await message.answer(f"💰 {coin.upper()} → {vs.upper()} = {price}")
