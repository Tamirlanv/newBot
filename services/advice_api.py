import requests

async def get_advice():
    try:
        resp = requests.get("https://api.adviceslip.com/advice")
        return resp.json()["slip"]["advice"]
    except:
        return "Ошибка получения совета."
