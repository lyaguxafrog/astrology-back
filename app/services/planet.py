# app/services/planet.py
import swisseph as swe

import os
from dotenv import load_dotenv, find_dotenv

from time_convert import get_julian_datetime

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Установка пути к эфемеридам
swe.set_ephe_path(os.getenv('EPH_PATH'))


class Planets:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int) -> None:
        """
        Конструктор класса Planets. Принимает параметры для инициализации объекта.

        :params year: Год
        :params month: Месяц
        :params day: День
        :params hour: Час
        :params minute: Минута
        """
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        
    # def start_end_position(self, planet_id: int):

    #     # Преобразования в Юлианский календарь
    #     start_jd_date = get_julian_datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute)
    #     end_jd_date = get_julian_datetime(year=self.year, month=self.month, day=self.day + 1, hour=self.hour, minute=self.minute)


    #     planet_names = {
    #         swe.SUN: "Sun",
    #         swe.MOON: "Moon",
    #         swe.MERCURY: "Mercury",
    #         swe.VENUS: "Venus",
    #         swe.MARS: "Mars",
    #         swe.JUPITER: "Jupiter",
    #         swe.SATURN: "Saturn",
    #         swe.URANUS: "Uranus",
    #         swe.NEPTUNE: "Neptune",
    #         swe.PLUTO: "Pluto",
    #         swe.MEAN_NODE: "Mean Node",
    #         swe.TRUE_NODE: "True Node"
    # }

    #     start_position = swe.calc_ut(start_jd_date, planet_id)
    #     end_position = swe.calc_ut(end_jd_date, planet_id)
    #     planet_name = planet_names[planet_id]

    #     return planet_name, planet_id, start_position, end_position

    


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
        
        julian_day_start = swe.julday(self.year, self.month, self.day, self.hour, self.minute, 0)
        julian_day_next = swe.julday(self.year, self.month, self.day + 1, self.hour, self.minute, 0)
        
        planet_positions = {}
        
        for planet_id in planet_names.keys():
            planet_position_start = swe.calc_ut(julian_day_start, planet_id)[0]
            planet_position_next = swe.calc_ut(julian_day_next, planet_id)[0]
            position_difference = planet_position_next - planet_position_start
            
            if position_difference < 0:
                retrograde = True
            else:
                retrograde = False
            
            daily_distance = abs(position_difference)
            distance_per_second = daily_distance / (24 * 3600)
            
            position_at_time = planet_position_start + (self.hour * 3600 + self.minute * 60 + self.second) * distance_per_second
            
            if retrograde:
                position_at_time -= (self.hour * 3600 + self.minute * 60 + self.second) * distance_per_second
            
            planet_positions[planet_names[planet_id]] = position_at_time
        
        return planet_positions

