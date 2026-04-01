from DataAccess.WeatherAPIClient import getWeatherData
from DataAccess.BesttimesAPIClient import getCrowdData

# Example coordinates for testing
location_name = "St. Thomas, Ontario"
lat = 42.7777
lon = -81.1827
print(f"---Getting weather for {location_name} (Lat: {lat}, Lon: {lon})---")
getWeatherData(lat, lon)



venue_name = "McDonald's"
venue_address = "Ocean Ave, San Francisco"
print(f"---Getting crowd data for {venue_name} at {venue_address}---")
getCrowdData(venue_name, venue_address)
