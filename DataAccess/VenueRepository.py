import os
import time
from dotenv import load_dotenv
import redis
import json

from DataAccess.BesttimesAPIClient import BesttimesAPIClient
from DataAccess.VenueAdapter import VenueAdapter
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

# saveVenueData will fetch new data from API, adapt it, and save to Redis with expiration
    def save_venue_data(self, venue_id, venue_name, venue_address):
        besttimes_client = BesttimesAPIClient()
        data = besttimes_client.get_besttimes_data(venue_name, venue_address)

        if data:
            # Use Adapter to convert raw API data to VenueDataObject
            venue_object = VenueAdapter.adapt(data)
            self.db.set(venue_id, json.dumps(venue_object.__dict__))
            return venue_object
            
        return None

# getCachedVenueData will return cached data if it exists and is not expired, otherwise it will call save_venue_data to fetch new data and cache it
    def get_cached_data(self, venue_name, venue_address):
        venue_id = f"venue:{venue_name.replace(' ', '_').lower()}"
        
        cached_json = self.db.get(venue_id)
        if cached_json:
            print(f"-     Cached {venue_name} data retrieved...")
            venue_dict = json.loads(cached_json)
            if time.time() - venue_dict.get("besttimes_timestamp", 0) < self.expiry_time:
                return VenueDataObject(**venue_dict)

        print(f"-     Fetching {venue_name} from BestTimes API...")
        return self.save_venue_data(venue_id, venue_name, venue_address)

