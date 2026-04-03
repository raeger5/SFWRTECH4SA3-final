################################################################################
# FieldDay - Main.py
#
# Purpose: Main entry point for the FieldDay application. 
#
# Author: Rachel Gerencser
# Contact: gerencrl@mcmaster.ca
#
################################################################################

from BusinessLogic.ScoreFactory import ScoreFactory
from BusinessLogic.TennisScorer import TennisScorer
from BusinessLogic.VolleyballScorer import VolleyballScorer
from BusinessLogic.SoccerScorer import SoccerScorer
from BusinessLogic.SoftballScorer import SoftballScorer
from DataAccess.WeatherAPIClient import WeatherAPIClient
from DataAccess.VenueRepository import VenueRepository

venue_repository = VenueRepository()
weather_api_client = WeatherAPIClient()
tennis_venues = [
    {"name": "Pickleball & Tennis Courts of Pinafore Park", "address": "31-41 Parkside Dr, St Thomas, ON N5R 1G5"},
    {"name": "Greenhills Tennis Centre", "address": "4838 Colonel Talbot Rd Unit B, London, ON N6P 1H7"},
    {"name": "Glanworth Park", "address": "6536 Bradish Rd, London, ON N6N 1N6"},
    # {"name": "Pickleball Courts at Burwell Park", "address": "465 Burwell Rd, St Thomas, ON N5P 4N6"},
]
beach_volleyball_venues = [
    {"name": "Port Stanley Beach", "address": "Lake Erie, 162 William St, Port Stanley, ON N5L 1E4"},
    {"name": "Boler Mountain", "address": "689 Griffith St, London, ON N6K 2S5"},
    # {"name": "1Password Park", "address": "355 Burwell Rd, St Thomas, ON N5P 4M3"},
]
softball_venues = [
    {"name": "Pinafore Park", "address": "31 Parkside Dr, St Thomas, ON N5R 1G5"},
    {"name": "Boler Mountain", "address": "689 Griffith St, London, ON N6K 2S5"},
    # {"name": "1Password Park", "address": "355 Burwell Rd, St Thomas, ON N5P 4M3"},
]
soccer_venues = [
    {"name": "Pinafore Park", "address": "31 Parkside Dr, St Thomas, ON N5R 1G5"},
    {"name": "Boler Mountain", "address": "689 Griffith St, London, ON N6K 2S5"},
    {"name": "Greenway Park", "address": "9 Pine Valley Dr, St Thomas, ON N5P 0A8"},
    ]

# This function will print the report for a given sport type. 
# It will fetch the venue data and weather data, calculate the scores, and print the leaderboard.
def print_venue_report(venues, sport_type):
    results = []
    for venue in venues:
        # Get venue data (with caching) and weather data, then calculate scores
        venue_data_object = venue_repository.get_cached_data(venue["name"], venue["address"])
        weather_data_object = weather_api_client.get_weather_data(venue_data_object.latitude, venue_data_object.longitude)
        
        # Use the ScoreFactory to get the appropriate scorer for the sport type, then calculate the scores
        scorer = ScoreFactory.create_scorer(sport_type)
        venue_score = scorer.calculate_crowd_score(venue_data_object)
        weather_score = scorer.calculate_weather_score(weather_data_object)
        score = scorer.calculate_score(venue_data_object, weather_data_object)
        
        # Store the results in a list for sorting and printing later
        results.append({
            "name": venue["name"],
            "score": score,
            "crowd_score": venue_score,
            "weather_score": weather_score
        })

    # Sort the list with highest score at index 0
    ranked_results = sorted(results, key=lambda x: x['score'], reverse=True)

    # Print the final leaderboard
    print("\n")
    print(f"--- {sport_type.upper()} VENUE RANKINGS ---")
    for i, entry in enumerate(ranked_results, 1):
        print(f"{i}. *{entry['score']:.2f}* {entry['name']} - *Crowd Score: {entry['crowd_score']:.2f} * Weather Score: {entry['weather_score']:.2f}*")
    print("\n")

def main():
    print("Welcome to FieldDay!")
    print("Your ultimate venue selection assistant for outdoor sports!")
    print("Let's find the best venues for your next game based on crowd levels and weather conditions.\n")
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

    
    
    while True:
        print("Select a report to view:")
        print("1. Tennis Report")
        print("2. Beach Volleyball Report")
        print("3. Softball Report")
        print("4. Soccer Report")
        print("0. Quit the application.")

        choice = input("Enter your choice (1-4): ")

        if choice == "0":
            print("Thank you for using FieldDay! Goodbye!")
            break

        if choice == "1":
            print_venue_report(tennis_venues, "tennis")

        elif choice == "2":
            print_venue_report(beach_volleyball_venues, "volleyball")

        elif choice == "3":           
            print_venue_report(softball_venues, "softball")

        elif choice == "4":
            print_venue_report(soccer_venues, "soccer")
  
if __name__ == "__main__":
    main()