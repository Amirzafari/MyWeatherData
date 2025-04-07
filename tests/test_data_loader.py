import unittest
from scripts.data_transformer import transform_weather_data
import pandas as pd

class TestDataTransformer(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {
                'city_name': 'New York',
                'country': 'US',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'temperature': 22.5,
                'humidity': 60,
                'pressure': 1015,
                'wind_speed': 5.1,
                'datetime': '2023-05-01T12:00:00'
            },
            {
                'city_name': 'London',
                'country': 'GB',
                'latitude': 51.5074,
                'longitude': -0.1278,
                'temperature': 15.3,
                'humidity': 72,
                'pressure': 1008,
                'wind_speed': 4.2,
                'datetime': '2023-05-01T12:00:00'
            }
        ]

    def test_transform_weather_data(self):
        fact_df, dim_df = transform_weather_data(self.test_data)

        # Test fact dataframe
        self.assertIsInstance(fact_df, pd.DataFrame)
        self.assertEqual(len(fact_df), 2)
        self.assertListEqual(list(fact_df.columns), ['date', 'time', 'city_id', 'temperature', 'humidity', 'pressure', 'wind_speed'])

        # Test dimension dataframe
        self.assertIsInstance(dim_df, pd.DataFrame)
        self.assertEqual(len(dim_df), 2)
        self.assertListEqual(list(dim_df.columns), ['city_id', 'city_name', 'country', 'latitude', 'longitude'])

        # Test data transformations
        self.assertEqual(fact_df['wind_speed'][0], 18.4)  # 5.1 m/s should be converted to 18.4 km/h
        self.assertEqual(fact_df['temperature'][0], 22.5)

if __name__ == '__main__':
    unittest.main()
    