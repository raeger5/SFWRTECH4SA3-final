
import time

from DataModel.VenueDataObject import VenueDataObject

class VenueAdapter:

    def adapt(besttimesData) -> VenueDataObject:
        return VenueDataObject(
            best_times_id=besttimesData['venue_info']['venue_id'],
            name=besttimesData['venue_info']['venue_name'],
            address=besttimesData['venue_info']['venue_address'],
            latitude=besttimesData['venue_info']['venue_lat'],
            longitude=besttimesData['venue_info']['venue_lon'],
            crowd_forecast=besttimesData['analysis'],
            besttimes_timestamp=time.time(),
        )   