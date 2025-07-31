import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, get_weather_icon, get_weather_description


class SimpleWeatherAppTest(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_weather_icon_mapping(self):
        """Test basic weather icon mapping"""
        self.assertEqual(get_weather_icon(0), "https://cdn-icons-png.flaticon.com/512/6974/6974833.png")
        self.assertEqual(get_weather_icon(999), "https://cdn-icons-png.flaticon.com/512/6974/6974833.png")  # Default
    
    def test_weather_description(self):
        """Test basic weather description mapping"""
        self.assertEqual(get_weather_description(0), "Clear sky")
        self.assertEqual(get_weather_description(999), "Unknown")
    
    @patch.dict(os.environ, {'CITY_NAME': 'TestCity'})
    @patch('app.requests.get')
    def test_api_response(self, mock_get):
        """Test basic API response"""
        # Mock geocoding response
        mock_geocoding = MagicMock()
        mock_geocoding.json.return_value = {
            "results": [{"latitude": 30.0, "longitude": 31.0}]
        }
        
        # Mock weather response
        mock_weather = MagicMock()
        mock_weather.json.return_value = {
            "current": {
                "temperature_2m": 25.5,
                "wind_speed_10m": 10.0,
                "relative_humidity_2m": 50.0,
                "weather_code": 1
            }
        }
        
        # Set up mock responses
        mock_get.side_effect = [mock_geocoding, mock_weather]
        
        # Test API call
        response = self.client.get('/api/weather', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['city'], 'TestCity')
        self.assertEqual(data['temperature'], 26)  # Rounded
    
    @patch.dict(os.environ, {'CITY_NAME': 'InvalidCity'})
    @patch('app.requests.get')
    def test_city_not_found(self, mock_get):
        """Test invalid city handling"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        
        response = self.client.get('/api/weather', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
