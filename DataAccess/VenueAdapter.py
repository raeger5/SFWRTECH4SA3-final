
import time

from DataModel.VenueDataObject import VenueDataObject
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="FieldDay_App")

class VenueAdapter:

    @staticmethod
    def adapt(besttimesData) -> VenueDataObject:
        venue_info = besttimesData.get('venue_info', {})
        
        return VenueDataObject(
            best_times_id=venue_info.get('venue_id', 'unknown'),
            name=venue_info.get('venue_name', 'Unknown Venue'),
            address=venue_info.get('venue_address', 'No Address Provided'),
            # Ensure these are floats for the Weather API
            latitude=float(venue_info.get('venue_lat', 0.0)),
            longitude=float(venue_info.get('venue_lon', 0.0)),
            crowd_forecast=besttimesData.get('analysis', {}),
            besttimes_timestamp=time.time(),
        )