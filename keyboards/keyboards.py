from aiogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌤 Погода"), KeyboardButton(text="💡 Совет")],
        [KeyboardButton(text="💵 Конвертер валют"), KeyboardButton(text="📋 Работа с Trello")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите опцию..."
)


trello_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🆕 Создать карточку", callback_data="create_card")
        ],
        [   InlineKeyboardButton(text="❌ Удалить", callback_data="delete_card"),
            InlineKeyboardButton(text="✏️ Обновить", callback_data="update_card"),
            InlineKeyboardButton(text="📋 Посмотреть карточки", callback_data="view_cards")
        ],
        [
            InlineKeyboardButton(text="📂 Переместить карточку", callback_data="move_card")
        ],
    ],
    resize_keyboard=True
)





