from datetime import datetime

from BusinessLogic.Scorer import Scorer
from DataModel.VenueDataObject import VenueDataObject
from DataModel.WeatherDataObject import WeatherDataObject

class SoftballScorer(Scorer):

    def calculate_score(self, venue_data_object: VenueDataObject, weather_data_object: WeatherDataObject) -> float:
        crowd_score = self.calculate_crowd_score(venue_data_object)
        weather_score = self.calculate_weather_score(weather_data_object)
        overall_score = (crowd_score * 0.8) + (weather_score * 0.2)
        return overall_score

    def calculate_crowd_score(self, venue_data_object: VenueDataObject) -> float:
        current_hour = datetime.now().hour
        return venue_data_object.get_todays_crowd_forecast()[current_hour]
    
    def calculate_weather_score(self, weather_data_object: WeatherDataObject) -> float:
        weather_score = 100
        # Penalty for high wind
        if weather_data_object.wind_speed > 10: 
            weather_score -= 20
        # Penalty for any precipitation
        if weather_data_object.precipitation > 0:
            weather_score -= 20  
        # Penalty for cold temperatures
        if weather_data_object.temperature < 10:
            weather_score -= 20
        return weather_score