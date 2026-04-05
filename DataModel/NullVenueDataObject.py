import datetime

from DataModel.VenueDataObject import VenueDataObject

class NullVenueDataObject(VenueDataObject):

    def __init__(self):
        super().__init__(
            best_times_id="null",
            name="Unknown Venue",
            address="No Address Available",
            latitude=0.0,
            longitude=0.0,
            crowd_forecast={i: {'day_raw': [0] * 24} for i in range(7)},  # Default to no crowds
            besttimes_timestamp=datetime.datetime.now().timestamp()
        )
        print(f"-     ⚠️  Cached data has no crowd data...")
        
    def get_todays_crowd_forecast(self):
        return [0] * 24
    
    def print_venue_data(self):
        print(f"\n🏞️  VENUE DATA:")
        print(f"\tNo venue data available")

    def print_crowd_forecast(self):
        print(f"\n👥 Crowd Forecast for {self.name}:")
        print(f"\tNo crowd data available for this venue")