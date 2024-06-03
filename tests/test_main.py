import unittest
import asyncio
import warnings
from parser import WeatherDataFetcher

class WeatherDataFetcherTestCase(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', category=ResourceWarning)
        self.weather_fetcher = WeatherDataFetcher('https://sheremetyevo.aeroport.website/pogoda')
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.weather_fetcher.fetch_data())
        self.weather_fetcher.parse_data()
    
    def check_result_type(self, result, expected_type):
        self.assertEqual(type(result), expected_type)

    def test_get_temperature(self):
        temperature = self.weather_fetcher.get_temperature()
        self.check_result_type(temperature, str)
        self.assertTrue('°C' in temperature, True)
        self.assertTrue(len(temperature) >= 1, True)

    def test_get_wind(self):
        wind = self.weather_fetcher.get_wind()
        self.check_result_type(wind, str)

    def test_get_temperature_status(self):
        temperature_status = self.weather_fetcher.get_temperature_status()
        self.check_result_type(temperature_status, str)

    def test_get_air_pressure(self):
        air_pressure = self.weather_fetcher.get_air_pressure()
        self.check_result_type(air_pressure, str)
        self.assertTrue('мм рт. ст.' in air_pressure, True)

