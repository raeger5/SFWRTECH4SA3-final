class WeatherDataObject:
    description: str
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    wind_speed: float
    precipitation: float
    humidity: int

    def __init__(self, description,temperature, feels_like, temp_min, temp_max, wind_speed, precipitation, humidity):
        self.description = description
        self.temperature = temperature
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.humidity = humidity

    def print_weather_data(self):
        print(f"\n🌤️  WEATHER DETAILS:")
        print(f"\tWeather Description: {self.description}")
        print(f"\tTemperature:         {self.temperature}°C") 
        print(f"\tFeels Like:          {self.feels_like}°C")
        print(f"\tMin Temperature:     {self.temp_min}°C")
        print(f"\tMax Temperature:     {self.temp_max}°C")
        print(f"\tWind Speed:          {self.wind_speed} m/s")
        print(f"\tPrecipitation:       {self.precipitation} mm")
        print(f"\tHumidity:            {self.humidity}%")


    