import datetime

from DataModel.VenueDataObject import VenueDataObject

class NullVenueDataObject(VenueDataObject):

    def __init__(self, **kwargs):
        super().__init__(
            best_times_id="null",
            name=kwargs.get('name', "Unknown Venue"),
            address=kwargs.get('address', "No Address Available"),
            latitude=kwargs.get('latitude', 0.0),
            longitude=kwargs.get('longitude', 0.0),
            crowd_forecast=kwargs.get('crowd_forecast', {i: {'day_raw': [0] * 24} for i in range(7)}),besttimes_timestamp=datetime.datetime.now().timestamp()
        )
        self.null_object = True
        print(f"-     ⚠️  Cached data has no crowd data...")
        
    def get_todays_crowd_forecast(self):
        return [0] * 24
    
    def print_venue_data(self):
        super().print_venue_data()
        print(f"\tNote: This is a cached venue object with no crowd data available.")

    def print_crowd_forecast(self):
        print(f"\n👥 Crowd Forecast for {self.name}:")
        print(f"\tNo crowd data available for this venue")