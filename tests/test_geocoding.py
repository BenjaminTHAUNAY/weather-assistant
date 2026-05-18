import pytest
from unittest.mock import patch, MagicMock
from tools.geocoding import get_coordinates


@patch('tools.geocoding.requests.get')
def test_get_coordinates_success(mock_get):
    """Test successful geocoding."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {'name': 'Riga', 'lat': 56.9496, 'lon': 24.1052, 'country': 'LV'}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = get_coordinates('Riga')
    
    assert result is not None
    assert result[0] == 56.9496
    assert result[1] == 24.1052


@patch('tools.geocoding.requests.get')
def test_get_coordinates_not_found(mock_get):
    """Test city not found."""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = get_coordinates('NonexistentCity12345')
    
    assert result is None


@patch('tools.geocoding.requests.get')
def test_get_coordinates_api_error(mock_get):
    """Test API error handling."""
    # Simulate a request exception (like network error)
    import requests
    mock_get.side_effect = requests.exceptions.RequestException('API Error')
    
    result = get_coordinates('Riga')
    
    assert result is None


def test_get_coordinates_no_api_key(monkeypatch):
    """Test error when API key is missing."""
    monkeypatch.setenv('OPENWEATHER_API_KEY', '')
    
    # Force reload to pick up new env var
    import importlib
    import tools.geocoding
    importlib.reload(tools.geocoding)
    
    with pytest.raises(ValueError, match="OPENWEATHER_API_KEY not found"):
        tools.geocoding.get_coordinates('Riga')