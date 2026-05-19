"""
Weather Agent - orchestrates tools to answer user queries
"""

import re
from tools import get_current_weather, get_forecast, get_coordinates


class WeatherAgent:
    """Agent that processes weather queries."""
    
    def __init__(self):
        self.last_query = None
        self.last_result = None
    
    def process_query(self, query: str) -> str:
        """
        Process a user query and return a weather report.
        
        Args:
            query: User query string (e.g., "weather in Paris", "forecast for London tomorrow")
            
        Returns:
            Formatted weather report string
        """
        self.last_query = query
        query_lower = query.lower()
        
        # Determine query type
        is_forecast = 'forecast' in query_lower or 'tomorrow' in query_lower or 'next' in query_lower
        
        # Extract city name
        city = self.extract_city(query)
        if not city:
            return "Error: Could not identify city name. Please specify a city (e.g., 'weather in Paris' or 'forecast for London')."
        
        # Get coordinates for better API accuracy
        coords = get_coordinates(city)
        if not coords:
            lat, lon = None, None
        else:
            lat, lon = coords
        
        if is_forecast:
            # Extract number of days (default 3)
            days_match = re.search(r'(\d+)\s*days?', query_lower)
            days = int(days_match.group(1)) if days_match else 3
            days = min(days, 5)
            
            result = get_forecast(city_name=city, lat=lat, lon=lon, days=days)
            if result:
                self.last_result = result
                return self.format_forecast(result, city)
            else:
                return f"Error: Could not fetch forecast for '{city}'. Please check the city name."
        else:
            result = get_current_weather(city_name=city, lat=lat, lon=lon)
            if result:
                self.last_result = result
                return self.format_current_weather(result)
            else:
                return f"Error: Could not fetch weather for '{city}'. Please check the city name."
    
    def extract_city(self, query: str) -> str | None:
        """Extract city name from query using simple patterns."""
        query_lower = query.lower()
        
        stop_words = ['weather', 'forecast', 'what', 'is', 'the', 'like', 'for', 'in', 'tomorrow', 'next', 'days', 'please', 'tell', 'me', 'about', 'give', 'current']
        
        # Pattern 1: "weather in CityName"
        match = re.search(r'weather\s+in\s+([A-Za-z\s-]+?)$', query_lower)
        if match:
            city = match.group(1).strip()
            if city and city not in stop_words and len(city) >= 2:
                return city.title()
        
        # Pattern 2: "forecast for CityName" or "weather for CityName"
        match = re.search(r'(?:weather|forecast)\s+for\s+([A-Za-z\s-]+?)(?:\s+for|\s+tomorrow|\s+next|\s+\d+\s*days?|$)', query_lower)
        if match:
            city = match.group(1).strip()
            city = re.sub(r'\s+(for|tomorrow|next|\d+)$', '', city)
            if city and city not in stop_words and len(city) >= 2:
                return city.title()
        
        # Pattern 3: "in CityName"
        match = re.search(r'in\s+([A-Za-z\s-]+?)(?:\s+for|\s+tomorrow|\s+next|\s+\d+\s*days?|$)', query_lower)
        if match:
            city = match.group(1).strip()
            city = re.sub(r'\s+(for|tomorrow|next|\d+)$', '', city)
            if city and city not in stop_words and len(city) >= 2:
                return city.title()
        
        # Pattern 4: "CityName weather" or "CityName forecast"
        words = query_lower.split()
        if len(words) >= 2 and words[1] in ['weather', 'forecast']:
            potential_city = words[0]
            if potential_city not in stop_words and len(potential_city) >= 2:
                return potential_city.title()
        
        return None

    def format_current_weather(self, data: dict) -> str:
        """Format current weather data into readable report."""
        report = f"""
╔════════════════════════════════════════╗
║         CURRENT WEATHER REPORT         ║
╠════════════════════════════════════════╣
║ City:     {data['city']}, {data['country']}
║ Temp:     {data['temperature']}°C (feels like {data['feels_like']}°C)
║ Humidity: {data['humidity']}%
║ Wind:     {data['wind_speed']} m/s
║ Pressure: {data['pressure']} hPa
║ Condition: {data['description'].capitalize()}
╚════════════════════════════════════════╝
"""
        if data['temperature'] < 0:
            report += "\n Recommendation: Very cold! Dress warmly and wear a coat."
        elif data['temperature'] < 10:
            report += "\n Recommendation: Cool weather. Bring a jacket."
        elif data['temperature'] < 20:
            report += "\n Recommendation: Pleasant weather. Enjoy your day!"
        elif data['temperature'] < 30:
            report += "\n Recommendation: Warm weather. Stay hydrated."
        else:
            report += "\n Recommendation: Very hot! Avoid prolonged sun exposure."
        
        if 'rain' in data['description'].lower():
            report += "\n Don't forget an umbrella!"
        elif 'snow' in data['description'].lower():
            report += "\n Wear boots and drive carefully."
        
        return report

    def format_forecast(self, forecast_data: list, city: str) -> str:
        """Format forecast data into readable report."""
        report = f"""
╔════════════════════════════════════════╗
║         WEATHER FORECAST REPORT        ║
║              {city.title()}                     ║
╠════════════════════════════════════════╣
"""
        for day in forecast_data:
            report += f"""
║ Date:     {day['date']}
║   Avg:    {day['avg_temp']}°C
║   Min:    {day['min_temp']}°C
║   Max:    {day['max_temp']}°C
║   Humidity: {day['avg_humidity']}%
║   Condition: {day['description'].capitalize()}
║  ──────────────────────────────────────
"""
        report += "╚════════════════════════════════════════╝"
        return report