from datetime import datetime

from BusinessLogic.Scorer import Scorer
from DataModel.VenueDataObject import VenueDataObject
from DataModel.WeatherDataObject import WeatherDataObject



class TennisScorer(Scorer):
    def calculate_score(self, venue_data_object: VenueDataObject, weather_data_object: WeatherDataObject) -> float:
        return 0
    