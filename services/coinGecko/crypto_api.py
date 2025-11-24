import requests
from dotenv import load_dotenv
import os

load_dotenv()

CG_API_KEY = os.getenv("CG_API_KEY")

url = "https://api.coingecko.com/api/v3/coins/list"

headers = {"x-cg-demo-api-key": CG_API_KEY}

response = requests.get(url, headers=headers)

print(response.json())