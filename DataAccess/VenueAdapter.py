import time

from DataModel.VenueDataObject import VenueDataObject
from geopy.geocoders import Nominatim

class VenueAdapter:
    
    @staticmethod
    def adapt(besttimesData) -> VenueDataObject:
        venue_info = besttimesData.get('venue_info', {})
        raw_analysis = besttimesData.get('analysis', {})

        # --- data normalization ---
        clean_forecast = {}
        
        # Check the type of raw_analysis
        is_list = isinstance(raw_analysis, list)

        for day_index in range(7):
            day_data = {}
            
            # If it's a list, access by index
            if is_list:
                if day_index < len(raw_analysis):
                    day_data = raw_analysis[day_index]
            # If it's a dict, use .get()
            elif isinstance(raw_analysis, dict):
                day_data = raw_analysis.get(day_index, {})
            
            # Ensure list of 24 zeros if 'day_raw' is missing
            day_raw = day_data.get('day_raw', [0] * 24) if isinstance(day_data, dict) else [0] * 24
            
            clean_forecast[day_index] = {'day_raw': day_raw}

        return VenueDataObject(
            best_times_id=venue_info.get('venue_id', 'null'),
            name=venue_info.get('venue_name', 'Unknown Venue'),
            address=venue_info.get('venue_address', 'No Address Provided'),
            latitude=float(venue_info.get('venue_lat', 0.0)),
            longitude=float(venue_info.get('venue_lon', 0.0)),
            crowd_forecast=clean_forecast, 
            besttimes_timestamp=time.time(),
        )