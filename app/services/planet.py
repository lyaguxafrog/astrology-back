# Импорт необходимых библиотек
import swisseph as swe
import os
from dotenv import load_dotenv, find_dotenv
from app.services.time_convert import get_julian_datetime, time_zone_convert

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Установка пути к файлам эфемерид
swe.set_ephe_path(os.getenv('EPH_PATH'))

# Определение класса Planets
class Planets:
    def __init__(self, year: int, month: int, day: int, hour: int,
                 minute: int, timezone: int) -> None:
        """
        Конструктор класса Planets. Принимает параметры для инициализации объекта.

        :params year: Год
        :params month: Месяц
        :params day: День
        :params hour: Час
        :params minute: Минута
        :params timezone: Смещение временной зоны по UTC в формате HH
        """
        # Инициализация переменных экземпляра
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = 0
        self.timezone = timezone

    def get_planet_positions(self):
        # Преобразование часа на основе временной зоны
        hour = time_zone_convert(int(self.hour), int(self.timezone))
        planet_position = []

        # Преобразование входной даты в начальную и следующую даты
        start_tjd_ut = get_julian_datetime(year=self.year, month=self.month, 
                                          day=self.day, 
                                          hour=self.hour, minute=self.minute)

        next_jid_ut = get_julian_datetime(year=self.year, month=self.month, 
                                          day=self.day + 1, 
                                          hour=self.hour, minute=self.minute)

        # Перебор идентификаторов планет
        for p in range(swe.SUN, swe.CHIRON + 1):
            if p == swe.EARTH:
                continue  # Пропустить Землю, так как она не нужна в данном контексте

            try:
                # Вычисление позиций планет в начальную и следующую даты
                start_dgr = swe.calc_ut(start_tjd_ut, p)[0][0]
                next_dgr = swe.calc_ut(next_jid_ut, p)[0][0]
            except swe.Error as err:
                continue  # Пропустить ошибки вычисления

            # Вычисление движения планеты за 24 часа и за секунду
            move_pear_24 = next_dgr - start_dgr
            move_pear_sec = move_pear_24 / 86400

            # Вычисление времени в секундах
            time = (hour * 3600) + (self.minute * 60)

            # Получение имени планеты
            pnam = swe.get_planet_name(p)

            # Определение типа движения планеты и конечной позиции
            if move_pear_24 < 0:
                planet_motion = ' R'  # Ретроградное движение
                end_planet_position = start_dgr - (time * move_pear_sec)
            else:
                planet_motion = ' None'  # Отсутствие ретроградного движения
                end_planet_position = start_dgr + (time * move_pear_sec)

            # Создание словаря для позиции планеты
            planet_position_dict = {
                "planet_id": p,
                "planet_name": pnam,
                "degree": end_planet_position,
                "retrograde": planet_motion
            }

            # Добавление позиции планеты в список
            planet_position.append(planet_position_dict)

        # Возврат списка позиций планет
        return planet_position
