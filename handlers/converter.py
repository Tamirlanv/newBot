from aiogram import Router, F
from services.currency_api import convert
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

router = Router()


valid_currencies = [
    "USD", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM",
    "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP",
    "BYN", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP", "CNH", "CNY", "COP", "CRC", "CUP",
    "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP",
    "FOK", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL",
    "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD",
    "JOD", "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT", "LAK",
    "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP",
    "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR",
    "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD",
    "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS",
    "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD",
    "TVD", "TWD", "TZS", "UAH", "UGX", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF",
    "XCD", "XCG", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMW", "ZWL"
]

valid_currency_pattern = r"(?i)^(" + "|".join(valid_currencies) + r")\s+"

@router.message(F.text == "💵 Конвертер валют")
async def kb_conv(message: Message):
    await message.answer(
        "Введите валюты в формате:\n"
        "`USD RUB`\n"
        "или\n"
        "`EUR KZT`",
        parse_mode="Markdown"
    )

@router.message(F.text.regexp(valid_currency_pattern))
async def currency_from_text(message: Message):
    text = message.text.strip().split()

    if len(text) == 2:
        base, target = text
        result = await convert(base.upper(), target.upper())
        kb = await currency_kb(base.upper())
        await message.answer(result, reply_markup=kb)
    else:
        await message.answer("Пожалуйста, введите 2 валюта, например: `USD RUB`.")
        
        
async def currency_kb(base):
    currencies = ['EUR', 'GBP', 'CNY', 'JPY', 'AUD', 'CAD', 'CHF', 'RUB', 'INR', 'KZT']
    keyboard = InlineKeyboardBuilder()
    for currency in currencies:
        if currency != base:  
            keyboard.add(InlineKeyboardButton(text=currency, callback_data=f"{base}_{currency}"))
    
    return keyboard.adjust(2).as_markup()

        
valid_callback_pattern = r"(?i)^[A-Z]{3}_[A-Z]{3}$"

        
@router.callback_query(F.data.regexp(valid_callback_pattern))
async def process_callback(query: CallbackQuery):
    base, target = query.data.split("_")
    result = await convert(base.upper(), target.upper())
    await query.message.edit_text(result, reply_markup=await currency_kb(base))
    await query.answer()