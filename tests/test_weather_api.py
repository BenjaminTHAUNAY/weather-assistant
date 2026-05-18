import pytest
from unittest.mock import patch, MagicMock
from tools.weather_api import get_current_weather, get_forecast


@patch('tools.weather_api.requests.get')
def test_get_current_weather_success(mock_get):
    """Test successful current weather retrieval."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'name': 'Riga',
        'main': {'temp': 15.5, 'feels_like': 14.2, 'humidity': 78, 'pressure': 1013},
        'weather': [{'description': 'light rain'}],
        'wind': {'speed': 5.2},
        'sys': {'country': 'LV'}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = get_current_weather(city_name='Riga')
    
    assert result is not None
    assert result['city'] == 'Riga'
    assert result['temperature'] == 15.5
    assert result['humidity'] == 78
    assert result['description'] == 'light rain'


@patch('tools.weather_api.requests.get')
def test_get_current_weather_with_coords(mock_get):
    """Test current weather with coordinates."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'name': 'Riga',
        'main': {'temp': 15.5, 'feels_like': 14.2, 'humidity': 78, 'pressure': 1013},
        'weather': [{'description': 'clear sky'}],
        'wind': {'speed': 3.0},
        'sys': {'country': 'LV'}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = get_current_weather(lat=56.95, lon=24.10)
    
    assert result is not None
    assert result['city'] == 'Riga'


@patch('tools.weather_api.requests.get')
def test_get_current_weather_api_error(mock_get):
    """Test handling of API error."""
    import requests
    mock_get.side_effect = requests.exceptions.RequestException('API Error')
    
    result = get_current_weather(city_name='Riga')
    
    assert result is None


def test_get_current_weather_no_params():
    """Test error when no parameters provided."""
    with pytest.raises(ValueError, match=r"Either city_name or \(lat, lon\) must be provided"):
        get_current_weather()


@patch('tools.weather_api.requests.get')
def test_get_forecast_success(mock_get):
    """Test successful forecast retrieval."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'list': [
            {'dt_txt': '2026-05-20 12:00:00', 'main': {'temp': 16.5}, 'weather': [{'description': 'clear sky'}], 'main': {'temp': 16.5, 'humidity': 70}},
            {'dt_txt': '2026-05-20 15:00:00', 'main': {'temp': 18.0, 'humidity': 65}, 'weather': [{'description': 'clear sky'}]},
            {'dt_txt': '2026-05-21 12:00:00', 'main': {'temp': 14.0, 'humidity': 80}, 'weather': [{'description': 'rain'}]},
        ]
    }
    # Fix: need to handle that each dict has its own 'main'
    # Recreate mock to avoid nested dict issues
    mock_response.json.return_value = {
        'list': [
            {'dt_txt': '2026-05-20 12:00:00', 'main': {'temp': 16.5, 'humidity': 70}, 'weather': [{'description': 'clear sky'}]},
            {'dt_txt': '2026-05-20 15:00:00', 'main': {'temp': 18.0, 'humidity': 65}, 'weather': [{'description': 'clear sky'}]},
            {'dt_txt': '2026-05-21 12:00:00', 'main': {'temp': 14.0, 'humidity': 80}, 'weather': [{'description': 'rain'}]},
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = get_forecast(city_name='Riga', days=2)
    
    assert result is not None
    assert len(result) == 2
    assert result[0]['date'] == '2026-05-20'
    assert result[1]['description'] == 'rain'


@patch('tools.weather_api.requests.get')
def test_get_forecast_api_error(mock_get):
    """Test forecast API error handling."""
    import requests
    mock_get.side_effect = requests.exceptions.RequestException('API Error')
    
    result = get_forecast(city_name='Riga')
    
    assert result is None