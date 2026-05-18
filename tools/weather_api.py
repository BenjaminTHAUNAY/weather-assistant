"""
Weather API tool - fetches current weather and forecasts
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_current_weather(city_name: str = None, lat: float = None, lon: float = None) -> dict | None:
    """
    Get current weather for a city or coordinates.
    
    Args:
        city_name: Name of the city (optional if lat/lon provided)
        lat: Latitude (optional if city_name provided)
        lon: Longitude (optional if city_name provided)
        
    Returns:
        Dictionary with weather data or None if error
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not found in environment variables")
    
    params = {'appid': API_KEY, 'units': 'metric'}
    
    if city_name:
        params['q'] = city_name
    elif lat is not None and lon is not None:
        params['lat'] = lat
        params['lon'] = lon
    else:
        raise ValueError("Either city_name or (lat, lon) must be provided")
    
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract and convert relevant data
        return {
            'city': data.get('name', 'Unknown'),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'country': data['sys'].get('country', '')
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")
        return None


def get_forecast(city_name: str = None, lat: float = None, lon: float = None, days: int = 3) -> list | None:
    """
    Get weather forecast for a city or coordinates.
    
    Args:
        city_name: Name of the city (optional if lat/lon provided)
        lat: Latitude (optional if city_name provided)
        lon: Longitude (optional if city_name provided)
        days: Number of days to return (max 5, API returns 3h intervals)
        
    Returns:
        List of daily forecast dictionaries or None if error
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not found in environment variables")
    
    params = {'appid': API_KEY, 'units': 'metric'}
    
    if city_name:
        params['q'] = city_name
    elif lat is not None and lon is not None:
        params['lat'] = lat
        params['lon'] = lon
    else:
        raise ValueError("Either city_name or (lat, lon) must be provided")
    
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process forecast data - group by day
        forecasts_by_day = {}
        
        for item in data['list']:
            date = item['dt_txt'].split()[0]  # YYYY-MM-DD
            
            if date not in forecasts_by_day:
                forecasts_by_day[date] = {
                    'temps': [],
                    'descriptions': [],
                    'humidities': []
                }
            
            forecasts_by_day[date]['temps'].append(item['main']['temp'])
            forecasts_by_day[date]['descriptions'].append(item['weather'][0]['description'])
            forecasts_by_day[date]['humidities'].append(item['main']['humidity'])
        
        # Convert to list of daily summaries
        result = []
        for i, (date, daily_data) in enumerate(list(forecasts_by_day.items())[:days]):
            result.append({
                'date': date,
                'avg_temp': round(sum(daily_data['temps']) / len(daily_data['temps']), 1),
                'min_temp': round(min(daily_data['temps']), 1),
                'max_temp': round(max(daily_data['temps']), 1),
                'description': daily_data['descriptions'][0],  # most common or first
                'avg_humidity': round(sum(daily_data['humidities']) / len(daily_data['humidities']))
            })
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Forecast API error: {e}")
        return None