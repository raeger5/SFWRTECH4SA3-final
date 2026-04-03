from abc import abstractmethod
from datetime import datetime

from DataModel.VenueDataObject import VenueDataObject
from DataModel.WeatherDataObject import WeatherDataObject

class Scorer:
    
    @abstractmethod
    def calculate_score(self, venue_data_object: VenueDataObject, weather_data_object: WeatherDataObject) -> float:
        pass

    def calculate_crowd_score(self, venue_data_object: VenueDataObject) -> float:
        current_hour = datetime.now().hour
        return venue_data_object.get_todays_crowd_forecast()[current_hour]

    @abstractmethod
    def calculate_weather_score(self, weather_data_object: WeatherDataObject) -> float:
        pass    