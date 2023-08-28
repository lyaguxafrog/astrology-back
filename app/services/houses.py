# Импорт необходимых библиотек
import swisseph as swe

import os
from dotenv import find_dotenv, load_dotenv

# Импорт функций из других модулей
from app.services.time_convert import get_julian_datetime, time_zone_convert
from app.services.maps_api import get_coordinates, extract_coordinates

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Установка пути к файлам эфемерид
swe.set_ephe_path(os.getenv('EPH_PATH'))

# Определение класса Houses
class Houses:
    def __init__(self, year: int, month: int, day: int,
                 hours: int, minute: int, timezone: int, place: str):
        """
        Конструктор класса Houses. Принимает параметры для инициализации объекта.

        :params year: Год
        :params month: Месяц
        :params day: День
        :params hours: Час
        :params minute: Минута
        :params timezone: Смещение временной зоны по UTC в формате HH
        :params place: Место для определения координат
        """
        self.year = year
        self.month = month
        self.day = day
        self.hours = time_zone_convert(hours, timezone)
        self.minute = minute
        self.place = place

    def get_house_name(self, house: bytes) -> str:
        """
        Получение названия Дома

        :params house: Код дома

        :returns: Название дома
        """
        house_name = swe.house_name(hsys=house)
        return house_name

    def get_house(self):
        # Список систем домов
        house_systems = [b"P", b"Y", b"X", b"H", b"C", b"F", b"B", b"D",
                         b"N", b"G", b"I", b"i", b"K", b"U", b"M", b"A", b"T",
                         b"O", b"L", b"Q", b"R", b"S", b"V", b"W"]

        houses_info = []

        # Преобразование даты и времени в юлианскую дату
        date = get_julian_datetime(year=self.year, month=self.month, day=self.day, hour=self.hours, minute=self.minute)

        # Получение координат из места
        coordinates = get_coordinates(self.place)
        latitude, longitude = extract_coordinates(coordinates)

        # Обход всех систем домов
        for house_system in house_systems:
            try:
                # Получение информации о доме с использованием указанной системы
                cusps, ascmc, cuspsspeed, ascmcspeed = swe.houses_ex2(tjdut=date,
                                                lat=latitude,
                                            lon=longitude, hsys=house_system,
                                            flags=0)
                house_name = self.get_house_name(house=house_system)

                # Создание словаря с информацией о доме
                house_info_dict = {
                    "system": house_system.decode(),
                    "name": house_name,
                    "cusps": cusps,
                    "ascmc": ascmc,
                    "cuspsspeed": cuspsspeed,
                    "ascmcspeed": ascmcspeed
                }

                houses_info.append(house_info_dict)
            except:
                if house_system == b"P" or b"K":
                    new_house_system = house_system
                    cusps, ascmc, cuspsspeed, ascmcspeed = swe.houses_ex2(tjdut=date, lat=latitude,
                                            lon=longitude, hsys=b"D",
                                            flags=0)
                    house_name = self.get_house_name(house=new_house_system)

                    house_info_dict = {
                    "system": house_system.decode(),
                    "name": house_name,
                    "cusps": cusps,
                    "ascmc": ascmc,
                    "cuspsspeed": cuspsspeed,
                    "ascmcspeed": ascmcspeed
                }   
                    houses_info.append(house_info_dict)

        return houses_info
