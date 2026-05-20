import pytest
from unittest.mock import patch, MagicMock
from agent import WeatherAgent


@patch('agent.get_coordinates')
@patch('agent.get_current_weather')
def test_process_query_current_weather(mock_weather, mock_geo):
    """Test full current weather query."""
    mock_geo.return_value = (56.95, 24.10)
    mock_weather.return_value = {
        'city': 'Riga',
        'country': 'LV',
        'temperature': 15.5,
        'feels_like': 14.2,
        'humidity': 78,
        'wind_speed': 5.2,
        'pressure': 1013,
        'description': 'light rain'
    }
    
    agent = WeatherAgent()
    result = agent.process_query("weather in Riga")
    
    assert 'Riga' in result
    assert '15.5' in result
    assert 'Light rain' in result
    mock_weather.assert_called_once()


@patch('agent.get_coordinates')
@patch('agent.get_forecast')
def test_process_query_forecast(mock_forecast, mock_geo):
    """Test full forecast query."""
    mock_geo.return_value = (56.95, 24.10)
    mock_forecast.return_value = [
        {
            'date': '2026-05-20',
            'avg_temp': 16.5,
            'min_temp': 12.0,
            'max_temp': 19.0,
            'avg_humidity': 70,
            'description': 'clear sky'
        }
    ]
    
    agent = WeatherAgent()
    result = agent.process_query("forecast for Riga")
    
    # Vérifier que le résultat contient les infos attendues
    assert 'Riga' in result
    assert '2026-05-20' in result
    assert 'Clear sky' in result or 'clear sky' in result
    mock_forecast.assert_called_once()


def test_process_query_no_city():
    """Test when no city can be extracted."""
    agent = WeatherAgent()
    result = agent.process_query("what is the weather like?")
    
    assert 'Error' in result
    assert 'Could not identify city' in result