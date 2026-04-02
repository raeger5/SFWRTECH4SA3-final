class VenueDataObject:
    def __init__(self, best_times_id, name, address, latitude, longitude, crowd_forecast, besttimes_timestamp):
        self.best_times_id = best_times_id
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.crowd_forecast = crowd_forecast 
        self.besttimes_timestamp = besttimes_timestamp


    def print_venue_data(self):
        print(f"BestTimes ID: {self.best_times_id}")
        print(f"Venue Name: {self.name}")
        print(f"Address: {self.address}")
        print(f"Latitude: {self.latitude}")
        print(f"Longitude: {self.longitude}")
        print(f"Crowd Forecast: {self.crowd_forecast}")
        
        