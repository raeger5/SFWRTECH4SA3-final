from abc import abstractmethod

from DataModel.VenueDataObject import VenueDataObject
from DataModel.WeatherDataObject import WeatherDataObject

class Scorer:
    @abstractmethod
    def calculate_score(self, venue_data_object: VenueDataObject, weather_data_object: WeatherDataObject) -> float:
        pass