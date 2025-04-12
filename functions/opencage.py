from opencage.geocoder import OpenCageGeocode
import os

async def address_to_coords(address):
    """
    Converts an address to coordinates using the OpenCage Geocoding API.

    Args:
        address: A string representing the address to convert.

    Returns:
        A tuple of floats representing the latitude and longitude of the address.
    """

    OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    result = geocoder.geocode(address)
    return {
        "lat": result[0]['geometry']['lat'],
        "lng": result[0]['geometry']['lng']
    }