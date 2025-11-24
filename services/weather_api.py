import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_KEY = os.getenv("WEATHER_API_KEY")

async def get_weather(city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric&lang=ru"
        resp = requests.get(url).json()

        if resp.get("cod") != 200:
            return "❌ Город не найден."

        desc = resp["weather"][0]["description"]
        temp = resp["main"]["temp"]

        w = desc.lower()

        if "дожд" in w or "rain" in w:
            emoji = "🌧"
        elif "облач" in w or "cloud" in w:
            emoji = "☁️"
        elif "ясно" in w or "clear" in w:
            emoji = "☀️"
        elif "snow" in w or "снег" in w:
            emoji = "❄️"
        elif "туман" in w or "fog" in w:
            emoji = "🌁"
        else:
            emoji = "🌡"

        return f"{emoji} Погода в городе {city.title()}\nОписание: {desc}\nТемпература: {temp}°C"

    except:
        return "❌ Ошибка при запросе погоды."
