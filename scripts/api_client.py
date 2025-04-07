import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
if not API_KEY:
    raise ValueError("OpenWeatherMap API key is not set in the .env file")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

CITIES = [
    {"name": "Austin", "country": "US"},
    {"name": "New York", "country": "US"},
    {"name": "London", "country": "GB"},
    {"name": "Tokyo", "country": "JP"},
    {"name": "Paris", "country": "FR"}
]

def fetch_weather_data():
    weather_data = []
    
    for city in CITIES:
        params = {
            'q': f"{city['name']},{city['country']}",
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                'city_name': city['name'],
                'country': city['country'],
                'latitude': data['coord']['lat'],
                'longitude': data['coord']['lon'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'datetime': datetime.utcfromtimestamp(data['dt']).isoformat()
            })
        else:
            print(f"Error fetching data for {city['name']}: {response.status_code}")
    
    return weather_data

if __name__ == "__main__":
    data = fetch_weather_data()
    for item in data:
        print(item)
