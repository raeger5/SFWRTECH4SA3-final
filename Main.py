################################################################################
# FieldDay - Main.py
#
# Purpose: Main entry point for the FieldDay application. 
#
# Author: Rachel Gerencser
# Contact: gerencrl@mcmaster.ca
#
################################################################################

from BusinessLogic.TennisScorer import TennisScorer
from BusinessLogic.VolleyballScorer import VolleyballScorer
from BusinessLogic.SoccerScorer import SoccerScorer
from BusinessLogic.SoftballScorer import SoftballScorer
from DataAccess.WeatherAPIClient import WeatherAPIClient
from DataAccess.VenueRepository import VenueRepository


# WELCOME TO FIELDDAY!
# 1. View Current Venue Group Reports
#   a. Venue Group 1
#   b. Venue Group 2
#   c. Venue Group 3
#   ...
# 2. Manage Venue Groups
#   a. Select Venue Group
#       i. Add Venue to Group
#       ii. Remove Venue from Group
#   b. Create New Venue Group
#   c. Delete Venue Group
# 3. Exit

venue_name = "McDonald's"
venue_address = "Ocean Ave, San Francisco"

venue_repository = VenueRepository()
venue_data_object = venue_repository.get_cached_data(venue_name, venue_address)
venue_data_object.print_venue_data()

weather_api_client = WeatherAPIClient()
weather_data_object = weather_api_client.get_weather_data(venue_data_object.latitude, venue_data_object.longitude)
weather_data_object.print_weather_data()

tennis_scorer = TennisScorer()
current_crowd_score = tennis_scorer.calculate_crowd_score(venue_data_object)
current_weather_score = tennis_scorer.calculate_weather_score(weather_data_object)
current_venue_score = tennis_scorer.calculate_score(venue_data_object, weather_data_object)
print(f"--TENNIS--")
print(f"Current Crowd Score: {current_crowd_score}")
print(f"Current Weather Score: {current_weather_score}")
print(f"Current Venue Score: {current_venue_score}")

volleyball_scorer = VolleyballScorer()
current_crowd_score = volleyball_scorer.calculate_crowd_score(venue_data_object)
current_weather_score = volleyball_scorer.calculate_weather_score(weather_data_object)      
current_venue_score = volleyball_scorer.calculate_score(venue_data_object, weather_data_object)
print(f"--VOLLEYBALL--")
print(f"Current Crowd Score: {current_crowd_score}")
print(f"Current Weather Score: {current_weather_score}")
print(f"Current Venue Score: {current_venue_score}")

softball_scorer = SoftballScorer()  
current_crowd_score = softball_scorer.calculate_crowd_score(venue_data_object)
current_weather_score = softball_scorer.calculate_weather_score(weather_data_object)
current_venue_score = softball_scorer.calculate_score(venue_data_object, weather_data_object)
print(f"--SOFTBALL--")
print(f"Current Crowd Score: {current_crowd_score}")
print(f"Current Weather Score: {current_weather_score}")
print(f"Current Venue Score: {current_venue_score}")

soccer_scorer = SoccerScorer()
current_crowd_score = soccer_scorer.calculate_crowd_score(venue_data_object)
current_weather_score = soccer_scorer.calculate_weather_score(weather_data_object)
current_venue_score = soccer_scorer.calculate_score(venue_data_object, weather_data_object)
print(f"--SOCCER--")
print(f"Current Crowd Score: {current_crowd_score}")
print(f"Current Weather Score: {current_weather_score}")
print(f"Current Venue Score: {current_venue_score}")