# app/services/maps_api.py
from ymaps import *
import os
import json
from dotenv import load_dotenv, find_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Получение ключа API из переменных окружения
apikey = os.getenv('MAP_API_KEY')

def search_location(place: str):
    """
    Поиск локации по API

    :params place: Место для прокидования по API

    :returns: JSON-ответ от API
    """

    client = GeocodeClient(api_key=apikey, timeout=10, lang="en_RU")

    finded_place = client.geocode(place)

    json_place = json.dumps(finded_place)

    return json_place

def extract_point_from_json(json_data):
    """
    Извлечение значения 'Point' из JSON-ответа

    :params json_data: JSON-ответ от API (словарь)

    :returns: Значение 'Point' как строку
    """
    try:
        feature_member = json_data['response']['GeoObjectCollection']['featureMember']
        if feature_member:
            point = feature_member[0]['GeoObject']['Point']['pos']
            return point
        else:
            return None
    except KeyError:
        return None

def get_coordinates(place: str):
    """
    Получение координат

    :params place: Место

    :returns: Координаты (Долгота и Широта)
    """

    # Пример использования
    json_response = {
        'response': {
            'GeoObjectCollection': {
                # ... ваш JSON-ответ здесь
            }
        }
    }

    point_value = extract_point_from_json(json_response)

    json_string = search_location(place)
    json_data = json.loads(json_string)

    point_value_from_api = extract_point_from_json(json_data)

    # Меняем порядок координат перед возвратом
    lon, lat = point_value_from_api.split()  # Разделяем координаты
    formatted_coordinates = f"{lat} {lon}"  # Меняем порядок и объединяем

    return formatted_coordinates

def extract_coordinates(coord_string):
    """
    Преобразование координат

    :params coord_string: Строка с долготой и широтой

    :returns: Кортеж с координатами (широта, долгота)
    """
    lat, lon = coord_string.split()  # Разделяем координаты по пробелу
    return float(lat), float(lon)  # Преобразуем в числа с плавающей точкой
