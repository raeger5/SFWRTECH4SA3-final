from DataModel import WeatherDataObject

class NullWeatherDataObject(WeatherDataObject):
    
    # A "Neutral" day that won't penalize any sport
    def __init__(self):
        super().__init__(
            description="No weather data available",
            temperature=20.0,  # Mild temperature
            feels_like=20.0,
            temp_min=15.0,
            temp_max=25.0,
            wind_speed=5.0,  # Light breeze
            precipitation=0.0,  # No rain
            humidity=50  # Moderate humidity
        )
        self.is_null = True


    