import pytest
from agent import WeatherAgent


def test_format_current_weather():
    """Test current weather formatting with rain."""
    agent = WeatherAgent()
    weather_data = {
        'city': 'Riga',
        'country': 'LV',
        'temperature': 15.5,
        'feels_like': 14.2,
        'humidity': 78,
        'wind_speed': 5.2,
        'pressure': 1013,
        'description': 'light rain'
    }
    
    result = agent.format_current_weather(weather_data)
    
    assert 'Riga' in result
    assert '15.5' in result
    assert 'Light rain' in result  # Changé: L majuscule
    assert 'umbrella' in result


def test_format_current_weather_cold():
    """Test cold weather formatting."""
    agent = WeatherAgent()
    weather_data = {
        'city': 'Riga',
        'country': 'LV',
        'temperature': -5,
        'feels_like': -8,
        'humidity': 85,
        'wind_speed': 3.0,
        'pressure': 1020,
        'description': 'snow'
    }
    
    result = agent.format_current_weather(weather_data)
    
    assert 'Very cold' in result
    assert 'Snow' in result  # Changé: S majuscule
    assert 'Boots' in result or 'boots' in result


def test_format_current_weather_hot():
    """Test hot weather formatting."""
    agent = WeatherAgent()
    weather_data = {
        'city': 'Riga',
        'country': 'LV',
        'temperature': 35,
        'feels_like': 38,
        'humidity': 40,
        'wind_speed': 2.0,
        'pressure': 1010,
        'description': 'clear sky'
    }
    
    result = agent.format_current_weather(weather_data)
    
    assert 'Very hot' in result
    assert 'Avoid prolonged sun' in result


def test_format_forecast():
    """Test forecast formatting."""
    agent = WeatherAgent()
    forecast_data = [
        {
            'date': '2026-05-20',
            'avg_temp': 16.5,
            'min_temp': 12.0,
            'max_temp': 19.0,
            'avg_humidity': 70,
            'description': 'clear sky'
        },
        {
            'date': '2026-05-21',
            'avg_temp': 14.0,
            'min_temp': 10.0,
            'max_temp': 16.0,
            'avg_humidity': 82,
            'description': 'rain'
        }
    ]
    
    result = agent.format_forecast(forecast_data, 'Riga')
    
    assert 'Riga' in result
    assert '2026-05-20' in result
    assert '2026-05-21' in result
    assert '16.5' in result
    assert 'Clear sky' in result  # Changé: C majuscule, s minuscule
    assert 'Rain' in result  # Ajouté pour vérifier aussi