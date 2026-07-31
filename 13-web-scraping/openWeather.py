import os

import requests
from dotenv import load_dotenv

LAT = 46.52417
LON = 6.55694
load_dotenv("../.env")
API_KEY = os.getenv("API_OPENWEATHER")
response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather?",
    params={"lat": LAT, "lon": LON, "appid": API_KEY},
)

from rich import print_json

print_json(response.text)
