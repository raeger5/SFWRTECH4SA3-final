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
from DataAccess.WeatherAPIClient import WeatherAPIClient
from DataAccess.VenueRepository import VenueRepository

venue_repository = VenueRepository()
weather_api_client = WeatherAPIClient()

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


# This function will print the report for a given sport type. 
# It will fetch the venue data and weather data, calculate the scores, and print the leaderboard.
def print_venue_report(venues, sport_type):
    results = []
    for venue in venues:
        print(f"\nProcessing {venue['name']}...")
        # Get venue data and weather data
        venue_data_object = venue_repository.get_cached_data(venue["name"], venue["address"])
        weather_data_object = weather_api_client.get_weather_data(venue_data_object.latitude, venue_data_object.longitude)
        
        # Use the ScoreFactory to get the scorer for the sport type, then calculate the scores
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
    # Header
    print("\n" + "="*85)
    if sport_type == "tennis":
        print(" 🎾  TENNIS POWER RANKINGS  🎾".center(85, " "))
    elif sport_type == "volleyball":
        print(" 🏐  BEACH VOLLEYBALL POWER RANKINGS  🏐".center(85, " "))
    elif sport_type == "softball":
        print(" 🥎  SOFTBALL POWER RANKINGS  🥎".center(85, " "))
    elif sport_type == "soccer":
        print(" ⚽  SOCCER POWER RANKINGS  ⚽".center(85, " ")) 
    print("="*85)
    
    # Table Column Headers
    # Format: Index (3), Name (40), Overall (10), Crowd (10), Weather (10)
    header = f"{'Rank':<5} {'Venue Name':<40} {'Score':>10} {'Crowd':>10} {'Weather':>10}"
    print(header)
    print("-" * 85)

    # Print the results
    for i, entry in enumerate(ranked_results, 1):
        if i == 1:
            rank_str = f"🥇 {i}"
            rank_padding = 4 
        else:
            rank_str = f"   {i}"
            rank_padding = 5

        name = entry['name']
        if len(name) > 38:
            name = name[:35] + "..."

        # Print with the dynamic rank_padding
        print(f"{rank_str:<{rank_padding}} {name:<40} {entry['score']:>10.1f} {entry['crowd_score']:>10.1f} {entry['weather_score']:>10.1f}")

    print("="*85 + "\n")

def main():
    print("Welcome to FieldDay!")
    print("Your ultimate venue selection assistant for outdoor sports!")
    print("Let's find the best venues for your next game based on crowd levels and weather conditions.\n")

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
            venues = venue_repository.get_venues_by_group("tennis")
            print_venue_report(venues, "tennis")

        elif choice == "2":
            venues = venue_repository.get_venues_by_group("volleyball")
            print_venue_report(venues, "volleyball")

        elif choice == "3":           
            venues = venue_repository.get_venues_by_group("softball")
            print_venue_report(venues, "softball")

        elif choice == "4":
            venues = venue_repository.get_venues_by_group("soccer")
            print_venue_report(venues, "soccer")
        else:
            print("Invalid choice. Please enter a number between 0 and 4.\n")   

if __name__ == "__main__":
    main()


# tennis_venues = [
#     {"name": "Pickleball & Tennis Courts of Pinafore Park", "address": "31-41 Parkside Dr, St Thomas, ON N5R 1G5"},
#     {"name": "Greenhills Tennis Centre", "address": "4838 Colonel Talbot Rd Unit B, London, ON N6P 1H7"},
#     {"name": "Glanworth Park", "address": "6536 Bradish Rd, London, ON N6N 1N6"},
#     # {"name": "Pickleball Courts at Burwell Park", "address": "465 Burwell Rd, St Thomas, ON N5P 4N6"},
# ]
# beach_volleyball_venues = [
#     {"name": "Port Stanley Beach", "address": "Lake Erie, 162 William St, Port Stanley, ON N5L 1E4"},
#     {"name": "Boler Mountain", "address": "689 Griffith St, London, ON N6K 2S5"},
#     # {"name": "1Password Park", "address": "355 Burwell Rd, St Thomas, ON N5P 4M3"},
# ]
# softball_venues = [
#     {"name": "Pinafore Park", "address": "31 Parkside Dr, St Thomas, ON N5R 1G5"},
#     {"name": "Boler Mountain", "address": "689 Griffith St, London, ON N6K 2S5"},
#     # {"name": "1Password Park", "address": "355 Burwell Rd, St Thomas, ON N5P 4M3"},
# ]
# soccer_venues = [
#     {"name": "Pinafore Park", "address": "31 Parkside Dr, St Thomas, ON N5R 1G5"},
#     {"name": "Boler Mountain", "address": "689 Griffith St, London, ON N6K 2S5"},
#     {"name": "Greenway Park", "address": "9 Pine Valley Dr, St Thomas, ON N5P 0A8"},
# ]

# initial_data = {
#     "tennis": tennis_venues,
#     "volleyball": beach_volleyball_venues,
#     "softball": softball_venues,
#     "soccer": soccer_venues
# }

# for sport, venues in initial_data.items():
#     for v in venues:
#         venue_repository.add_venue_to_group(sport, v["name"], v["address"])