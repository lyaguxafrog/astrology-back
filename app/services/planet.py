# app/services/planet.py
import swisseph as swe

import os
from dotenv import load_dotenv, find_dotenv

from app.services.time_convert import get_julian_datetime

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Установка пути к эфемеридам
swe.set_ephe_path(os.getenv('EPH_PATH'))


class Planets:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, timezone: int) -> None:
        """
        Конструктор класса Planets. Принимает параметры для инициализации объекта.

        :params year: Год
        :params month: Месяц
        :params day: День
        :params hour: Час
        :params minute: Минута
        :params timezone: Смещение временной зоны по UTC в формате HH
        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = 0
        self.timezone = timezone
        
 


    def get_planet_positions(self):
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
        
        julian_day_start = swe.julday(self.year, self.month, self.day, 0, 0)  # Start of the day
        julian_day_next = swe.julday(self.year, self.month, self.day + 1, 0, 0)  # Start of the next day
        
        planet_positions = {}
        
        for planet_id in planet_names.keys():
            planet_position_start = swe.calc_ut(julian_day_start, planet_id)[0][0]
            planet_position_next = swe.calc_ut(julian_day_next, planet_id)[0][0]
            position_difference = planet_position_next - planet_position_start
            
            if position_difference < 0:
                position_difference += 360.0
            
            daily_distance = abs(position_difference)
            distance_per_second = daily_distance / (24 * 3600)
            
            target_time_seconds = (self.hour - self.timezone) * 3600 + self.minute * 60 + self.second
            position_at_start = planet_position_start + target_time_seconds * distance_per_second
            
            if position_at_start > 360.0:
                position_at_start -= 360.0
            
            planet_positions[planet_names[planet_id]] = position_at_start
        
        return planet_positions