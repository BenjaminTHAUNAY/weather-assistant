"""
Geocoding tool - converts city name to coordinates
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"


def get_coordinates(city_name: str) -> tuple[float, float] | None:
    """
    Convert city name to latitude and longitude.
    
    Args:
        city_name: Name of the city (e.g., "Paris", "London")
        
    Returns:
        Tuple of (latitude, longitude) or None if city not found
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not found in environment variables")
    
    params = {
        'q': city_name,
        'limit': 1,
        'appid': API_KEY
    }
    
    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return None
        
        lat = data[0].get('lat')
        lon = data[0].get('lon')
        
        return (lat, lon)
        
    except requests.exceptions.RequestException as e:
        print(f"Geocoding error: {e}")
        return None