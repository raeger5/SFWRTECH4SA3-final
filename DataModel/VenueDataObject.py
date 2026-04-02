import datetime

class VenueDataObject:
    best_times_id: str
    name: str
    address: str
    latitude: float
    longitude: float
    crowd_forecast: dict
    besttimes_timestamp: float

    def __init__(self, best_times_id, name, address, latitude, longitude, crowd_forecast, besttimes_timestamp):
        self.best_times_id = best_times_id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.crowd_forecast = crowd_forecast 
        self.besttimes_timestamp = besttimes_timestamp

    def get_todays_crowd_forecast(self):
        today_index = datetime.datetime.now().weekday()
        try:
            return self.crowd_forecast[today_index].get('day_raw', [])
        except (KeyError, TypeError):
            return 0

    def print_venue_data(self):
        print(f"BestTimes ID: {self.best_times_id}")
        print(f"Venue Name: {self.name}")
        print(f"Address: {self.address}")
        print(f"Latitude: {self.latitude}")
        print(f"Longitude: {self.longitude}")
        print(f"Crowd Forecast: {self.crowd_forecast}")
        
        