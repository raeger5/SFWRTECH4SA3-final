import os
import requests
from dotenv import load_dotenv
from DataModel.WeatherDataObject import WeatherDataObject
load_dotenv()

class WeatherAPIClient:
    def __init__(self):
        
        self.API_KEY = os.getenv("WEATHER_API_KEY")


    def get_weather_data(self, lat, lon):
        print("Fetching weather data...")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric"

        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(data)
            return WeatherDataObject(
                description=data['weather'][0].get('description', 'No description available'),
                temperature=data['main']['temp'],
                feels_like=data['main']['feels_like'],
                temp_min=data['main']['temp_min'],
                temp_max=data['main']['temp_max'],
                wind_speed=data['wind']['speed'],
                precipitation=data.get('rain', {}).get('1h', 0), 
                humidity=data['main']['humidity'],
            )
        
        else:
            print(f"Error {response.status_code}: {response.json().get('message')}")
            return None

