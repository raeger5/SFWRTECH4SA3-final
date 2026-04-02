import os
from dotenv import load_dotenv
import requests


class BesttimesAPIClient:
    
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('BESTTIMES_API_KEY')

    def get_besttimes_data(self, venue_name, address):
        url = "https://besttime.app/api/v1/forecasts"
        
        params = {
            'api_key_private': self.API_KEY,
            'venue_name': venue_name,
            'venue_address': address
        }

        response = requests.post(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
    