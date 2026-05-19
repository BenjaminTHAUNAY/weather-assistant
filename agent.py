"""
Weather Agent - orchestrates tools to answer user queries
"""

import re


class WeatherAgent:
    """Agent that processes weather queries."""
    
    def __init__(self):
        self.last_query = None
        self.last_result = None
    
    def extract_city(self, query: str) -> str | None:
        """Extract city name from query using simple patterns."""
        query_lower = query.lower()
        
        # Pattern: "in CityName"
        match = re.search(r'in\s+([A-Za-z\s-]+?)(?:\s+for|\s+tomorrow|\s+next|$)', query_lower)
        if match:
            return match.group(1).strip().title()
        
        # Pattern: "for CityName"
        match = re.search(r'for\s+([A-Za-z\s-]+?)(?:\s+tomorrow|\s+next|$)', query_lower)
        if match:
            return match.group(1).strip().title()
        
        # Pattern: "CityName weather" or "CityName forecast"
        match = re.search(r'^([A-Za-z\s-]+?)\s+(weather|forecast)', query_lower)
        if match:
            return match.group(1).strip().title()
        
        # Pattern: "weather in CityName"
        match = re.search(r'weather\s+in\s+([A-Za-z\s-]+?)$', query_lower)
        if match:
            return match.group(1).strip().title()
        
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
        # Recommendation logic
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