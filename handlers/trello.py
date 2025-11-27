from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.instances import trello_client
from services.trello.trello_api import TrelloAPI
from database import *
from keyboards.keyboards import trello_kb

router = Router()

# ---------------- FSM ----------------

class TrelloAuth(StatesGroup):
    waiting_key = State()
    waiting_token = State()
    choose_board = State()

class TrelloCreate(StatesGroup):
    choose_list = State()
    enter_name = State()

class TrelloDelete(StatesGroup):
    choose_card = State()

class TrelloUpdate(StatesGroup):
    choose_card = State()
    enter_name = State()

class TrelloMove(StatesGroup):
    choose_card = State()
    choose_list = State()


# ---------------- Helpers ----------------

async def get_api(user_id, message=None):
    keys = get_trello_keys(user_id)
    if not keys:
        if message:
            await message.answer("❗ Сначала нужно авторизоваться и ввести ключи Trello.")
        return None
    key, token = keys
    return TrelloAPI(key, token, trello_client)


# ---------------- AUTH ----------------

@router.message(F.text == "📋 Работа с Trello")
async def trello_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    key, token = get_trello_keys(user_id)

    if key and token:
        await message.answer("✔️ Ключ и токен Trello уже сохранены!")
        await message.answer("Выберите действие:", reply_markup=trello_kb)
        return

    await message.answer("У вас не найден Trello API KEY.\nВведите ваш API Key:")
    await state.set_state(TrelloAuth.waiting_key)


@router.message(TrelloAuth.waiting_key)
async def trello_got_key(message: Message, state: FSMContext):
    await state.update_data(trello_key=message.text)
    await message.answer("Теперь введите Trello TOKEN:")
    await state.set_state(TrelloAuth.waiting_token)


@router.message(TrelloAuth.waiting_token)
async def trello_got_token(message: Message, state: FSMContext):
    data = await state.get_data()

    save_trello_keys(
        user_id=message.from_user.id,
        key=data["trello_key"],
        token=message.text
    )

    api = await get_api(message.from_user.id)

    boards = await api.client.get(
        "https://api.trello.com/1/members/me/boards",
        params=api._auth()
    )

    if not boards:
        await message.answer("Не удалось получить список досок. Проверьте ключ и токен.")
        await state.clear()
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=b["name"], callback_data=f"select_board_{b['id']}")]
            for b in boards
        ]
    )

    await message.answer("Выберите доску для работы:", reply_markup=kb)
    await state.set_state(TrelloAuth.choose_board)
    
    
@router.callback_query(TrelloAuth.choose_board, F.data.startswith("select_board_"))
async def select_board(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    board_id = cb.data.split("select_board_", 1)[1]

    save_board_id(cb.from_user.id, board_id)

    await cb.message.answer("📌 Доска выбрана и сохранена!")
    await cb.message.answer("Выберите действие:", reply_markup=trello_kb)

    await state.clear()

# ---------------- VIEW CARDS ----------------

@router.callback_query(F.data == "view_cards")
async def view_cards(cb: CallbackQuery):
    await cb.answer()
    api = await get_api(cb.from_user.id, cb.message)
    if not api:
        return

    board_id = get_board_id(cb.from_user.id)
    if not board_id:
        await cb.message.answer("❗ Board ID не задан.")
        return

    cards = await api.get_cards(board_id)
    if not cards:
        await cb.message.answer("Карточек нет.")
        return

    text = "\n".join(f"• {c['name']} (id={c['id']})" for c in cards)
    await cb.message.answer(text)


# ---------------- CREATE CARD ----------------

@router.callback_query(F.data == "create_card")
async def create_card_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    api = await get_api(cb.from_user.id, cb.message)
    if not api:
        return

    board_id = get_board_id(cb.from_user.id)
    if not board_id:
        await cb.message.answer("❗ Board ID не задан.")
        return

    lists = await api.get_lists(board_id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=l["name"], callback_data=f"create_in_{l['id']}")]
            for l in lists
        ]
    )
    await cb.message.answer("Выберите список:", reply_markup=kb)
    await state.set_state(TrelloCreate.choose_list)
    

@router.callback_query(TrelloCreate.choose_list, F.data.startswith("create_in_"))
async def create_choose_list(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    list_id = cb.data.split("_", 2)[2]
    await state.update_data(list_id=list_id)
    await cb.message.answer("Введите название новой карточки:")
    await state.set_state(TrelloCreate.enter_name)
    

@router.message(TrelloCreate.enter_name)
async def create_card_finish(message: Message, state: FSMContext):
    api = await get_api(message.from_user.id, message)
    if not api:
        return

    data = await state.get_data()
    await api.create_card(message.text, data["list_id"])
    await message.answer("✅ Карточка создана!")
    await state.clear()


# ---------------- DELETE CARD ----------------

@router.callback_query(F.data == "delete_card")
async def delete_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    api = await get_api(cb.from_user.id, cb.message)
    if not api:
        return

    board_id = get_board_id(cb.from_user.id)
    if not board_id:
        await cb.message.answer("❗ Board ID не задан.")
        return

    cards = await api.get_cards(board_id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c["name"], callback_data=f"del_{c['id']}")]
            for c in cards
        ]
    )
    await cb.message.answer("Выберите карточку:", reply_markup=kb)
    await state.set_state(TrelloDelete.choose_card)
    

@router.callback_query(TrelloDelete.choose_card, F.data.startswith("del_"))
async def delete_finish(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    card_id = cb.data.split("_", 1)[1]
    api = await get_api(cb.from_user.id, cb.message)
    if not api:
        return

    await api.delete_card(card_id)
    await cb.message.answer("✅ Карточка удалена!")
    await state.clear()


# ---------------- UPDATE CARD ----------------

@router.callback_query(F.data == "update_card")
async def update_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    api = await get_api(cb.from_user.id, cb.message)
    if not api:
        return

    board_id = get_board_id(cb.from_user.id)
    cards = await api.get_cards(board_id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c["name"], callback_data=f"upd_{c['id']}")]
            for c in cards
        ]
    )
    await cb.message.answer("Выберите карточку:", reply_markup=kb)
    await state.set_state(TrelloUpdate.choose_card)
    

@router.callback_query(TrelloUpdate.choose_card, F.data.startswith("upd_"))
async def update_select(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    card_id = cb.data.split("_", 1)[1]
    await state.update_data(card_id=card_id)
    await cb.message.answer("Введите новое имя:")
    await state.set_state(TrelloUpdate.enter_name
                          )

@router.message(TrelloUpdate.enter_name)
async def update_finish(message: Message, state: FSMContext):
    api = await get_api(message.from_user.id, message)
    if not api:
        return

    data = await state.get_data()
    await api.update_card(data["card_id"], message.text)
    await message.answer("✅ Название обновлено!")
    await state.clear()


# ---------------- MOVE CARD ----------------

@router.callback_query(F.data == "move_card")
async def move_start(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    api = await get_api(cb.from_user.id, cb.message)
    if not api:
        return

    board_id = get_board_id(cb.from_user.id)
    cards = await api.get_cards(board_id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=c["name"], callback_data=f"mv_{c['id']}")]
            for c in cards
        ]
    )
    await cb.message.answer("Выберите карточку:", reply_markup=kb)
    await state.set_state(TrelloMove.choose_card)
    

@router.callback_query(TrelloMove.choose_card, F.data.startswith("mv_"))
async def move_choose_list(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    card_id = cb.data.split("_", 1)[1]
    await state.update_data(card_id=card_id)

    api = await get_api(cb.from_user.id, cb.message)
    board_id = get_board_id(cb.from_user.id)
    lists = await api.get_lists(board_id)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=l["name"], callback_data=f"mv_to_{l['id']}")]
            for l in lists
        ]
    )
    await cb.message.answer("Выберите новый список:", reply_markup=kb)
    await state.set_state(TrelloMove.choose_list)
    

@router.callback_query(TrelloMove.choose_list, F.data.startswith("mv_to_"))
async def move_finish(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    list_id = cb.data.split("_", 2)[2]
    data = await state.get_data()

    api = await get_api(cb.from_user.id, cb.message)
    await api.move_card(data["card_id"], list_id)
    await cb.message.answer("✅ Карточка перемещена!")
    await state.clear()
