import os
from dotenv import load_dotenv
import requests

load_dotenv()

geocode_api_key = os.getenv("GEOCODE_API_KEY")

def get_coordinates(state:str,city:str):
    url = f"https://geocode.maps.co/search?city={city}&state={state}&&country=India&api_key={geocode_api_key}"
    response = requests.get(url)
    data = response.json()

    if data :
        return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"])
                }
    else:
       raise ValueError("Cant fetch geocoding data")

