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
            day_data = self.crowd_forecast.get(today_index) or self.crowd_forecast.get(str(today_index))
            return day_data.get('day_raw', [0] * 24)
        except (AttributeError, KeyError):
            return [0] * 24

    def print_venue_data(self):
        print(f"\n🏞️  VENUE DATA:")
        print(f"\tVenue Name:     {self.name}")
        print(f"\tAddress:        {self.address}")
        print(f"\tLatitude:       {self.latitude}")
        print(f"\tLongitude:      {self.longitude}")

    def print_crowd_forecast(self):
        print(f"\n👥 Crowd Forecast for {self.name}:")
        forecast = self.get_todays_crowd_forecast()
        for hour, level in enumerate(forecast):
            time_label = f"{(hour % 12 or 12)}{'AM' if hour < 12 else 'PM'}"
            print(f"\t{time_label:>4} - {level:>3}%")
        
        