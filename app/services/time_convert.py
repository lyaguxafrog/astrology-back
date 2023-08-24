# Импорт необходимых библиотек
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import math
import pytz


def get_time_zone(latitude: float, longitude: float) -> int:
    """
    Получение часового пояса UTC в формате HH

    :params latitude: Широта
    :params longitude: Долгота

    :returns: Час смещения
    """
    # Создание объекта TimezoneFinder для определения часового пояса
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)

    # Если не удалось определить часовой пояс
    if timezone_str is None:
        return None

    # Получение текущей даты и времени в указанном часовом поясе
    now = datetime.now(pytz.timezone(timezone_str))
    utc_offset = int(now.utcoffset().total_seconds() / 3600)

    return utc_offset


def get_julian_datetime(year: int, month: int, day: int,
                        hour: int, minute: int) -> float:
    """
    Конвертация даты и времени в Юлианский календарь

    :params year: Год
    :params month: Месяц      
    :params day: День
    :params hour: Час  
    :params minute: Минута

    :returns: Дата в Юлианском календаре
    """
    # Создание объекта datetime для заданных параметров
    date = datetime(year=year, month=month, day=day,
                    hour=hour, minute=minute, second=0)

    # Проверка типа входных данных
    if not isinstance(date, datetime):
        raise TypeError(
            'Invalid type for parameter "date" - expecting datetime'
        )
    # Проверка на диапазон года
    elif date.year < 1801 or date.year > 2099:
        raise ValueError(
            'Datetime must be between year 1801 and 2099'
        )

    # Вычисление Юлианской даты
    julian_datetime = 367 * date.year - int(
        (7 * (date.year + int(
            (date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (
        date.hour + date.minute / 60.0 + date.second / math.pow(
            60, 2)) / 24.0 - 0.5 * math.copysign(
        1, 100 * date.year + date.month - 190002.5) + 0.5

    return julian_datetime


def time_zone_convert(hour: int, zone: int) -> int:
    """
    Конвертация времени из одного часового пояса в другой

    :params hour: Час
    :params zone: Смещение часового пояса

    :returns: Новый час после конвертации
    """

    # Вычисление нового часа с учетом смещения
    new_time = (hour - zone) % 24
    
    # Если новый час получился отрицательным, добавляем 24 часа
    if new_time < 0:
        new_time += 24
        
    return new_time