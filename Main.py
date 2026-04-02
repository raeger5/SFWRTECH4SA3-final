################################################################################
# FieldDay - Main.py
#
# Purpose: Main entry point for the FieldDay application. 
#
# Author: Rachel Gerencser
# Contact: gerencrl@mcmaster.ca
#
################################################################################

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

