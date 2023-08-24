import unittest
from datetime import datetime
import json
from ymaps import *

from app.services.time_convert import get_time_zone, get_julian_datetime, time_zone_convert
from app.services.houses import Houses
from app.services.planet import Planets
from unittest.mock import patch
from app.services.maps_api import search_location, extract_point_from_json, get_coordinates, extract_coordinates



class TestTimeConvert(unittest.TestCase):

    def test_get_time_zone(self):
        # Тестирование функции get_time_zone
        # Точные координаты могут измениться, поэтому здесь используются примерные значения
        latitude = 52.5200
        longitude = 13.4050
        utc_offset = get_time_zone(latitude, longitude)
        self.assertIsInstance(utc_offset, int)
        self.assertGreaterEqual(utc_offset, -12)  # Минимальное смещение -12 часов
        self.assertLessEqual(utc_offset, 14)  # Максимальное смещение +14 часов

    def test_get_julian_datetime(self):
        # Тестирование функции get_julian_datetime
        year = 2023
        month = 8
        day = 24
        hour = 12
        minute = 0
        julian_date = get_julian_datetime(year, month, day, hour, minute)
        self.assertIsInstance(julian_date, float)
        self.assertGreater(julian_date, 2450000)  # Примерное минимальное значение
        self.assertLess(julian_date, 2500000)  # Примерное максимальное значение

    def test_time_zone_convert(self):
        # Тестирование функции time_zone_convert

        # Проверка конвертации в положительное смещение
        hour = 12
        zone = 3
        new_hour = time_zone_convert(hour, zone)
        self.assertEqual(new_hour, 9)  # 12 - 3 = 

        # Проверка конвертации в отрицательное смещение
        hour = 6
        zone = -2
        new_hour = time_zone_convert(hour, zone)
        self.assertEqual(new_hour, 8)  # 6 - (-2) = 8

        # Проверка конвертации при переходе через полночь
        hour = 2
        zone = 4
        new_hour = time_zone_convert(hour, zone)
        self.assertEqual(new_hour, 22)  # 2 - 4 = 22

class TestHouses(unittest.TestCase):
    def test_get_house_name(self):
        houses = Houses(2023, 8, 24, 12, 0, 3, "Moscow, Russia")
        house_name = houses.get_house_name(b"B")
        self.assertEqual(house_name, "Alcabitius")  # Исправленное значение

    def test_get_house(self):
        houses = Houses(2023, 8, 24, 12, 0, 3, "Moscow, Russia")
        houses_info = houses.get_house()
        self.assertEqual(len(houses_info), 24)  # Ожидаем 24 системы домов

class TestPlanets(unittest.TestCase):
    def test_get_planet_positions(self):
        planets = Planets(2023, 8, 24, 12, 0, 3)
        planet_positions = planets.get_planet_positions()
        
        # Проверка, что список позиций планет не пустой
        self.assertTrue(len(planet_positions) > 0)
        
        # Проверка, что для каждой планеты добавлено имя и позиция
        for planet in planet_positions:
            self.assertIn("planet_name", planet)
            self.assertIn("degree", planet)
        
        # Проверка, что долгота планеты находится в допустимом диапазоне
        for planet in planet_positions:
            degree = planet["degree"]
            self.assertGreaterEqual(degree, 0)
            self.assertLessEqual(degree, 360)


class TestMapsAPI(unittest.TestCase):

    @patch('app.services.maps_api.search_location', return_value='{"response": {"GeoObjectCollection": {"featureMember": [{"GeoObject": {"Point": {"pos": "37.615560 55.752220"}}}]}}}')
    def test_get_coordinates(self, mock_search_location):
        coordinates = get_coordinates("Moscow, Russia")
        self.assertEqual(coordinates, "55.752220 37.615560")

    def test_extract_coordinates(self):
        coordinates = "55.752220 37.615560"
        lat, lon = extract_coordinates(coordinates)
        self.assertEqual(lat, 55.752220)
        self.assertEqual(lon, 37.615560)


if __name__ == '__main__':
    unittest.main()