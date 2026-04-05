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


def main():
    # ** INSTRUCTIONS **
    # MAKE SURE YOU HAVE THE ENV VARIABLES SET UP IN YOUR .env FILE BEFORE RUNNING THE PROGRAM.

    # 1. ON FIRST RUN or TO RESEED: uncomment the following line to seed the initial venue groups in Redis, then re-comment it for future runs to preserve your data.
    # reset_initial_data()
    
    # 2. Run the program and select option 1 to view venue group reports.

    # 3. Select option 2 to manage venue groups, and select option 1 to add a venue, and specify the sport type.
    #   When adding a venue, make sure to copy & paste the name and address exactly as they appear on Google Maps for best results.
    #   You can try any of these sample venues or add your own:
    #       name | address
    #       * these will work and create a complete VenueDataObject with coordinates from the API:
    #       "Pickleball & Tennis Courts of Pinafore Park" | "31-41 Parkside Dr, St Thomas, ON N5R 1G5"
    #       "Greenhills Tennis Centre" | "4838 Colonel Talbot Rd Unit B, London, ON N6P 1H7"
    #       "Glanworth Park" | "6536 Bradish Rd, London, ON N6N 1N6"
    #       "Port Stanley Beach" | "Lake Erie, 162 William St, Port Stanley, ON N5L 1E4"
    #       "Boler Mountain" | "689 Griffith St, London, ON N6K 2S5"
    #       "Pinafore Park" | "31 Parkside Dr, St Thomas, ON N5R 1G5"
    #       "Greenway Park" | "9 Pine Valley Dr, St Thomas, ON N5P 0A8"

    #       * these will trigger the manual entry flow since they are not recognized by the API, but you can still add them by entering coordinates manually:
    #           If you choose to add a venue manually, you will need to enter the latitude and longitude coordinates. 
    #           You can find these by searching for the venue on Google Maps, right-clicking on the location, and selecting "What's here?" 
    #           The coordinates will be displayed at the bottom of the screen.
    #       "Pickleball Courts at Burwell Park" | "465 Burwell Rd, St Thomas, ON N5P 4N6"
    #       "1Password Park" | "355 Burwell Rd, St Thomas, ON N5P 4M3" -> lat: 42.7719, lon: -81.1908
    
    # 5. After adding a venue, select option 1 to view the updated reports and see how the new venue ranks against the others in its group.

    # 6. You can also remove venues from groups by selecting option 2 and then option 2 again, and following the prompts.
 
    
    print("\n🎉  Welcome to FieldDay! 🎉")
    print("Your ultimate venue selection assistant for outdoor sports!")
    print("Let's find the best venues for your next game based on crowd levels and weather conditions.\n")

    while True:
        print("\n==================================================")
        print("🏠 MAIN MENU")
        print("1. 🏆 View Venue Group Reports")
        print("2. ⚙️  Manage Venue Groups")
        print("0. 🚪 Exit")
        print("==================================================")
        choice = input("Enter your choice (1-2): ")

        if choice == "0":
            print("👋 Thank you for using FieldDay! Goodbye!")
            break

        # Option 1: View Venue Group Reports
        if choice == "1":
            view_reports_menu()        
        
        # Option 2: Manage Venue Groups
        elif choice == "2":
            manage_groups_menu()
       
        else:
            print("Invalid choice. Please enter a number between 0 and 4.\n")   

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
            "weather_score": weather_score,
            "venue_data": venue_data_object,
            "weather_data": weather_data_object
        })

    # Sort the list with highest score at index 0
    ranked_results = sorted(results, key=lambda x: x['score'], reverse=True)

    # Print the final leaderboard
    # Header
    print("\n" + "="*85)
    if sport_type == "tennis":
        print(" 🎾  TENNIS VENUE RANKINGS  🎾".center(85, " "))
    elif sport_type == "volleyball":
        print(" 🏐  BEACH VOLLEYBALL VENUE RANKINGS  🏐".center(85, " "))
    elif sport_type == "softball":
        print(" 🥎  SOFTBALL VENUE RANKINGS  🥎".center(85, " "))
    elif sport_type == "soccer":
        print(" ⚽  SOCCER VENUE RANKINGS  ⚽".center(85, " ")) 
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
        if getattr(entry['venue_data'], 'null_object', False):
            crowd_display = "N/A"
        else:
            crowd_display = f"{entry['crowd_score']:.1f}"
        print(f"{rank_str:<{rank_padding}} {name:<40} {entry['score']:>10.1f} {crowd_display:>10} {entry['weather_score']:>10.1f}")

    print_data_menu(ranked_results)

def print_data_menu(ranked_results):
    while True:
        print("\n📊 View Raw Data for Venue")
        choice = input("Enter your a venue rank to see details or hit 0 to go back: ")

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(ranked_results):
                selected = ranked_results[index]
                venue_data = selected['venue_data']
                weather_data = selected['weather_data']

                print("\n" + "-"*50)
                print(f"📍 RAW DATA: {selected['name'].upper()}")
                print("-"*50)
                
                # --- Venue Data ---
                venue_data.print_venue_data()

                # --- Weather Data ---
                weather_data.print_weather_data()
    
                # --- Crowd Data ---
                venue_data.print_crowd_forecast()
                
            else:
                print("❌ Invalid choice. Please pick a number from the list.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def view_reports_menu():
    while True:
        print("\n==================================================")
        print("🏆 View Venue Group Reports")
        print("1. 🎾 Tennis Report")
        print("2. 🏐 Beach Volleyball Report")
        print("3. 🥎 Softball Report")
        print("4. ⚽ Soccer Report")
        print("0. ⬅️  Back")
        print("==================================================")

        report_choice = input("Enter your choice (1-4): ")

        if report_choice == "0":
            return

        if report_choice == "1":
            venues = venue_repository.get_venues_by_group("tennis")
            print_venue_report(venues, "tennis")

        elif report_choice == "2":
            venues = venue_repository.get_venues_by_group("volleyball")
            print_venue_report(venues, "volleyball")

        elif report_choice == "3":           
            venues = venue_repository.get_venues_by_group("softball")
            print_venue_report(venues, "softball")

        elif report_choice == "4":
            venues = venue_repository.get_venues_by_group("soccer")
            print_venue_report(venues, "soccer")
        
        


def manage_groups_menu():
    while True:
        print("\n==================================================")
        print("⚙️  Manage Venue Groups")
        print("1. ➕ Add Venue to Group")
        print("2. ➖ Remove Venue from Group")
        print("0. ⬅️  Back")
        print("==================================================")
        manage_choice = input("Enter your choice (1-2): ")

        if manage_choice == "0":
            return

        if manage_choice == "1":
            add_venues_to_groups_menu()

        elif manage_choice == "2":
            remove_venues_from_groups_menu()
            
def add_venues_to_groups_menu():
    while True:
        print("\n==================================================")
        print("➕ Which group would you like to add a venue to?")
        print("1. 🎾 Tennis")
        print("2. 🏐 Beach Volleyball")
        print("3. 🥎 Softball")
        print("4. ⚽ Soccer")
        print("0. ⬅️  Back")
        print("==================================================")
        group_choice = input("Enter your choice (1-4): ")

        if group_choice == "0":
            return

        group_mapping = {
            "1": "tennis",
            "2": "volleyball",
            "3": "softball",
            "4": "soccer"
        }

        if group_choice in group_mapping:
            group_name = group_mapping[group_choice]
            print("* Search on google maps and copy & paste the following details exactly:")
            venue_name = input("Enter the NAME of the venue: ")
            venue_address = input("Enter the ADDRESS of the venue: ")        
            venue_repository.add_venue_to_group(group_name, venue_name, venue_address)

        input("Press Enter to continue...")
        return

def remove_venues_from_groups_menu():
    while True:
        print("\n==================================================")
        print("➖ Which group would you like to remove a venue from?")
        print("1. 🎾 Tennis")
        print("2. 🏐 Beach Volleyball")
        print("3. 🥎 Softball")
        print("4. ⚽ Soccer")
        print("0. ⬅️  Back")
        print("==================================================")
        group_choice = input("Enter your choice (1-4): ")

        if group_choice == "0":
            return
        
        group_mapping = {
            "1": "tennis",
            "2": "volleyball",
            "3": "softball",
            "4": "soccer"
        }

        if group_choice in group_mapping:
            group_name = group_mapping[group_choice]
            index = 1
            for venue in venue_repository.get_venues_by_group(group_name):
                print(f"{index}. {venue['name']} ({venue['address']})")
                index += 1
            venue_number = int(input("Enter the index of the venue you want to remove: "))
            venue_to_remove = venue_repository.get_venues_by_group(group_name)[venue_number - 1]
            venue_repository.remove_venue_from_group(group_name, venue_to_remove["name"], venue_to_remove["address"])

        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")

        input("Press Enter to continue...")
        return
    
def reset_initial_data():
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
    initial_data = {
        "tennis": tennis_venues,
        "volleyball": beach_volleyball_venues,
        "softball": softball_venues,
        "soccer": soccer_venues
    }

    sports_to_reset = ["tennis", "volleyball", "softball", "soccer"]
    print("Clearing venue groups in Redis...")
    for sport in sports_to_reset:
        current_venues = venue_repository.get_venues_by_group(sport)
        for venue in current_venues:
            venue_repository.remove_venue_from_group(sport, venue["name"], venue["address"])
    print("Seeding fresh initial data...")
    for sport, venues in initial_data.items():
        for v in venues:
            venue_repository.add_venue_to_group(sport, v["name"], v["address"])
            

if __name__ == "__main__":
    main()


