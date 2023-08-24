# app/services/planet.py
import swisseph as swe

import os
from dotenv import load_dotenv, find_dotenv

from app.services.time_convert import get_julian_datetime, time_zone_convert

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


        hour = time_zone_convert(int(self.hour), int(self.timezone))
        planet_position = []

        _isvalid, start_tjd_ut, start_dt = swe.date_conversion(self.year, self.month, self.day, 0.0)
        _isvalid, next_jid_ut, next_dt = swe.date_conversion(self.year, self.month, self.day + 1, 0.0)

        for p in range(swe.SUN, swe.CHIRON + 1):
            if p == swe.EARTH:
                continue
            
            try:
                start_dgr = swe.calc_ut(start_tjd_ut, p)[0][0]
                next_dgr = swe.calc_ut(next_jid_ut, p)[0][0]
            except swe.Error as err:
                continue

            move_pear_24 = next_dgr - start_dgr
            move_pear_sec = move_pear_24 /  86400

            time = (hour * 3600) + (self.minute * 60)

            pnam = swe.get_planet_name(p)

            if move_pear_24 < 0:
                planet_motion = ' R'
                end_planet_position = start_dgr - (time * move_pear_sec)
            else:
                planet_motion = ' None'
                end_planet_position = start_dgr + (time * move_pear_sec)

            planet_position_dict = {
                "planet_id": p,
                "planet_name": pnam,
                "degree": end_planet_position,
                "retrograde": planet_motion
            }
            
            planet_position.append(planet_position_dict)

        return planet_position