# app/services/planet.py
import swisseph as swe

import os
from dotenv import load_dotenv, find_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Установка пути к эфемеридам
swe.set_ephe_path(os.getenv('EPH_PATH'))

def calculate_planet_position(hours: int, day: int, month: int, year: int, planet_id):
    """
    Получение данных о планетах по времени

    :params hour: Час
    :params day: День
    :params month: Месяц
    :params year: Год

    :returns: Список всех планет
    """

    planet_names = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MERCURY: "Mercury",
    swe.VENUS: "Venus",
    swe.MARS: "Mars",
    swe.JUPITER: "Jupiter",
    swe.SATURN: "Saturn",
    swe.URANUS: "Uranus",
    swe.NEPTUNE: "Neptune",
    swe.PLUTO: "Pluto",
    swe.MEAN_NODE: "Mean Node",
    swe.TRUE_NODE: "True Node"
}

    # Вычисляем юлианскую дату в терминах эфемеридного времени (ET)
    jd_start = swe.julday(year, month, day, hours)
    jd_end = swe.julday(year, month, day + 1, hours)  # Конец дня

    # Рассчитываем позицию планеты на начало и конец дня
    start_planet_position, _ = swe.calc_ut(jd_start, planet_id)  # Игнорируем второй элемент
    end_planet_position, _ = swe.calc_ut(jd_end, planet_id)  # Игнорируем второй элемент

    # Рассчитываем разницу позиций и переводим её в градусы
    position_difference = end_planet_position[0] - start_planet_position[0]
    if position_difference < 0:
        position_difference += 360.0

    # Рассчитываем скорость планеты (градусы в сутки)
    planet_speed = position_difference / 1.0  # Перевод в градусы в сутки

    # Рассчитываем сколько градусов планета прошла за заданное время
    elapsed_hours = hours - start_planet_position[0]
    if elapsed_hours < 0:
        elapsed_hours += 360.0

    # Рассчитываем позицию планеты на заданное время
    current_planet_position = start_planet_position[0] + (planet_speed * elapsed_hours)

    return planet_id, planet_names[planet_id], current_planet_position

def calculate_planet_degrees(planet_positions):
    """
    Вычисление градусов планет из позиций планет

    :params planet_positions: Список позиций планет

    :returns: Словарь с градусами планет
    """
    planet_degrees = {}
    
    for planet_pos in planet_positions:
        planet_id = planet_pos['planet_id']
        longitude = planet_pos['longitude']
        planet_degrees[planet_id] = longitude
    
    return planet_degrees
