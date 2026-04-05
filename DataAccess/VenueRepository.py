import os
import time
from dotenv import load_dotenv
import redis
import json

from DataAccess.BesttimesAPIClient import BesttimesAPIClient
from DataAccess.VenueAdapter import VenueAdapter
from DataModel.NullVenueDataObject import NullVenueDataObject
from DataModel.VenueDataObject import VenueDataObject
load_dotenv()

class VenueRepository:
    def __init__(self):
        self.db = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )
        self.expiry_time = 604800  # 1 week in seconds

# Check if the API response contains coordinates. If not, prompt the user to enter them manually. 
# It then injects the coordinates back into the raw data so that the Adapter can find them during adaptation.
    def _ensure_coordinates(self, data, name):
        v_info = data.get('venue_info', {})
        lat = v_info.get('venue_lat')
        lon = v_info.get('venue_lon')

        if not lat or not lon:
            print(f"⚠️ Warning: Coordinates not found for {name}.")
            choice = input("Would you like to (1) Enter manually or (2) Cancel: ")
            
            if choice == "1":
                lat = float(input("Enter Latitude: "))
                lon = float(input("Enter Longitude: "))
                # Inject them into the raw data so the Adapter can find them
                data['venue_info']['venue_lat'] = lat
                data['venue_info']['venue_lon'] = lon
                return True
            return False # User cancelled
        return True # Coordinates were already there

# saveVenueData will fetch new data from API, adapt it, and save to Redis with expiration
    def save_venue_data(self, venue_id, venue_name, venue_address):
        besttimes_client = BesttimesAPIClient()
        data = besttimes_client.get_besttimes_data(venue_name, venue_address)

        # CASE 1: API found the venue
        if data and data.get('status') == "OK":
            venue_object = VenueAdapter.adapt(data)
            self.db.set(venue_id, json.dumps(venue_object.__dict__))
            return venue_object
            
        # CASE 2: API 404 or Failure - Offer Manual Entry
        print(f"⚠️  BestTimes API could not find crowd data for '{venue_name}'.")
        confirm = input("Would you like to add it manually with coordinates only? (y/n): ").lower()
        
        if confirm == 'y':
            try:
                lat = float(input("Enter Latitude (e.g., 42.77): "))
                lon = float(input("Enter Longitude (e.g., -81.19): "))
                
                # Create a Null Object but inject the real name and coordinates so that the Adapter can use them
                manual_data = {
                    "venue_info": {
                        "venue_id": "null", 
                        "venue_name": venue_name,
                        "venue_address": venue_address,
                        "venue_lat": lat,
                        "venue_lon": lon
                    },
                    "analysis": {} # This triggers the Adapter's 24-zero logic
                }

                manual_venue = VenueAdapter.adapt(manual_data)
                self.db.set(venue_id, json.dumps(manual_venue.__dict__))
                return manual_venue
            
            except ValueError:
                print("❌ Invalid coordinates. Manual add failed.")
        
        return None # Truly cancelled

# getCachedVenueData will return cached data if it exists and is not expired, otherwise it will call save_venue_data to fetch new data and cache it
    def get_cached_data(self, venue_name, venue_address):
        venue_id = f"venue:{venue_name.replace(' ', '_').lower()}"
        
        cached_json = self.db.get(venue_id)
        if cached_json:
            print(f"-     Fetching cached venue data...")
            venue_dict = json.loads(cached_json)
            if venue_dict.get('best_times_id') == "null":
                return NullVenueDataObject(**venue_dict) 
            if time.time() - venue_dict.get("besttimes_timestamp", 0) < self.expiry_time:
                return VenueDataObject(**venue_dict)

        print(f"-     Fetching fresh data from BestTimes API...")
        result = self.save_venue_data(venue_id, venue_name, venue_address)
        return result if result else NullVenueDataObject()
    

# Venue Group Management Methods
    def get_venues_by_group(self, group_name: str) -> list:
        group_key = f"group:{group_name.lower()}"
        venue_jsons = self.db.smembers(group_key)
        return [json.loads(v) for v in venue_jsons]

    def add_venue_to_group(self, group_name: str, name: str, address: str):
        if not name.strip() or not address.strip():
            print("Error: Venue name and address cannot be blank.")
            return

        group_key = f"group:{group_name.lower()}"
        venue_id = f"venue:{name.replace(' ', '_').lower()}"
        
        print(f"🔍 Validating {name} with BestTimes API...")
        result = self.save_venue_data(venue_id, name, address)
        
        # Only add to the group if a real VenueDataObject or NullVenueDataObject with coordinates was returned
        if result is not None:
            venue_data = json.dumps({"name": name, "address": address})
            self.db.sadd(group_key, venue_data)
            print(f"✅ Success! {name} has been added to the {group_name} group.")
        else:
            print(f"⚠️ Action Cancelled: {name} was not added to the group.")
            

    def remove_venue_from_group(self, group_name: str, name: str, address: str):
        group_key = f"group:{group_name.lower()}"
        venue_data = json.dumps({"name": name, "address": address})
        self.db.srem(group_key, venue_data)
        print(f"✅ Success! {name} has been removed from the {group_name} group.")
