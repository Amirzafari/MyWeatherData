import unittest
from unittest.mock import patch, Mock
from scripts.api_client import fetch_weather_data, CITIES

class TestApiClient(unittest.TestCase):

    @patch('scripts.api_client.requests.get')
    def test_fetch_weather_data(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "coord": {"lat": 40.7128, "lon": -74.0060},
            "main": {"temp": 22.5, "humidity": 60, "pressure": 1015},
            "wind": {"speed": 5.1},
            "dt": 1620000000  # Example timestamp
        }
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_weather_data()

        # Assertions
        self.assertEqual(len(result), len(CITIES))
        self.assertEqual(result[0]['city_name'], CITIES[0]['name'])
        self.assertEqual(result[0]['country'], CITIES[0]['country'])
        self.assertEqual(result[0]['temperature'], 22.5)
        self.assertEqual(result[0]['humidity'], 60)
        self.assertEqual(result[0]['pressure'], 1015)
        self.assertEqual(result[0]['wind_speed'], 5.1)

    @patch('scripts.api_client.requests.get')
    def test_fetch_weather_data_api_error(self, mock_get):
        # Mock an API error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_weather_data()

        # Assertions
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
    