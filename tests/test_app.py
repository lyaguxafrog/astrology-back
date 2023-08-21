import unittest
from app.services import maps_api, houses, planet, time_convert

class TestMapsApi(unittest.TestCase):

    def test_search_location(self):
        # Тестирование поиска локации
        result = maps_api.search_location("Moscow, Russia")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)  # Проверяем, что результат является строкой

    def test_extract_point_from_json(self):
        # Тестирование извлечения точки из JSON-ответа
        json_data = {
            'response': {
                'GeoObjectCollection': {
                    'featureMember': [
                        {
                            'GeoObject': {
                                'Point': {
                                    'pos': '55.7558 37.6173'
                                }
                            }
                        }
                    ]
                }
            }
        }
        point = maps_api.extract_point_from_json(json_data)
        self.assertEqual(point, '55.7558 37.6173')

class TestHouses(unittest.TestCase):

    def test_get_house(self):
        result = houses.get_house(2023, 1, 1, 12, 0, b'P', 55.7558, 37.6173)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)  # Проверяем, что результат - кортеж

    def test_get_house_name(self):
        # Тестирование получения названия дома
        house_name = houses.get_house_name(b'B')
        self.assertEqual(house_name, 'Alcabitius')

class TestTimeConvert(unittest.TestCase):

    def test_get_julian_datetime(self):
        # Тестирование конвертации даты в Юлианский календарь
        result = time_convert.get_julian_datetime(2023, 1, 1, 12, 0)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, float)  # Проверяем, что результат - число с плавающей точкой

    def test_time_zone_convert(self):
        # Тестирование конвертации таймзоны в UTC
        result = time_convert.time_zone_convert(12, 'UTC+03:00')
        self.assertEqual(result, 15)

class TestPlanet(unittest.TestCase):

    def test_get_planets(self):
        # Тестирование получения данных о планетах
        result = planet.get_planets(12, 1, 1, 2023)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)  # Проверяем, что результат - список
        self.assertGreater(len(result), 0)  # Проверяем, что список не пуст

    def test_calculate_planet_degrees(self):
        # Тестирование вычисления градусов планет
        planet_positions = [
            {"planet_id": 0, "longitude": 10.5, "latitude": 0.0},
            {"planet_id": 1, "longitude": 20.5, "latitude": 0.0},
            {"planet_id": 2, "longitude": 30.5, "latitude": 0.0},
        ]
        result = planet.calculate_planet_degrees(planet_positions)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)  # Проверяем, что результат - словарь
        self.assertEqual(result[0], 10.5)
        self.assertEqual(result[1], 20.5)
        self.assertEqual(result[2], 30.5)

if __name__ == '__main__':
    unittest.main()