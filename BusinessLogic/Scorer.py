from abc import abstractmethod

from DataModel.VenueDataObject import VenueDataObject
from DataModel.WeatherDataObject import WeatherDataObject

class Scorer:
    
    @abstractmethod
    def calculate_score(self, venue_data_object: VenueDataObject, weather_data_object: WeatherDataObject) -> float:
        pass

    @abstractmethod
    def calculate_crowd_score(self, venue_data_object: VenueDataObject) -> float:
        pass

    @abstractmethod
    def calculate_weather_score(self, weather_data_object: WeatherDataObject) -> float:
        pass    