import os
import requests
from dotenv import load_dotenv

# Load  variables from  .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

API_KEY = os.environ.get('WEATHER_API_KEY')

def getWeatherData(lat, lon):
    print("Fetching weather data...")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    
    else:
        print(f"Error {response.status_code}: {response.json().get('message')}")
        return None
