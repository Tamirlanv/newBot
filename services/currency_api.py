import os
import requests
from dotenv import load_dotenv

load_dotenv()


EXR_KEY = os.getenv("EXR_API_KEY")

async def convert(base, target):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXR_KEY}/latest/{base}"
        resp = requests.get(url).json()

        if resp.get("result") != "success":
            return "⚠️ Ошибка: неверная валюта."

        rate = resp["conversion_rates"].get(target)
        if not rate:
            return "⚠️ Валюта не найдена."

        return f"💵 1 {base} = {rate} {target}"

    except Exception:
        return "❌ Не удалось получить курс валют."
