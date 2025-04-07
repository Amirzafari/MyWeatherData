import unittest
from unittest.mock import patch, MagicMock
from scripts.data_loader import load_data
import pandas as pd

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.fact_df = pd.DataFrame({
            'date': ['2023-05-01', '2023-05-01'],
            'time': ['12:00:00', '12:00:00'],
            'city_id': [0, 1],
            'temperature': [22.5, 15.3],
            'humidity': [60, 72],
            'pressure': [1015, 1008],
            'wind_speed': [18.36, 15.12]
        })

        self.dim_df = pd.DataFrame({
            'city_id': [0, 1],
            'city_name': ['New York', 'London'],
            'country': ['US', 'GB'],
            'latitude': [40.7128, 51.5074],
            'longitude': [-74.0060, -0.1278]
        })

    @patch('scripts.data_loader.create_engine')
    def test_load_data(self, mock_create_engine):
        # Mock the database connection and execution
        mock_conn = MagicMock()
        mock_create_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

        # Call the function
        load_data(self.fact_df, self.dim_df)

        # Assert that execute was called for each row in both dataframes
        self.assertEqual(mock_conn.execute.call_count, len(self.fact_df) + len(self.dim_df))

if __name__ == '__main__':
    unittest.main()
    