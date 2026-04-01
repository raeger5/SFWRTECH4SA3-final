import os
from dotenv import load_dotenv
import requests

# Load  variables from  .env file
load_dotenv()
API_KEY = os.getenv('BESTTIMES_API_KEY')

def getCrowdData(venue_name, address):
    url = "https://besttime.app/api/v1/forecasts"
    
    params = {
        'api_key_private': API_KEY,
        'venue_name': venue_name,
        'venue_address': address
    }

    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
    