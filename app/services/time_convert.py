# app/services/time_convert.py
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import math


def get_time_zone(latitude: float, longitude: float) -> int:
    """
    Получения часового пояса UTC в формате HH

    :params latitude: Широта
    :params longitude: Долгота

    :returns: Час смешения
    """
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)

    if timezone_str is None:
        return None

    from datetime import datetime
    import pytz

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

    if not isinstance(date, datetime):
        raise TypeError(
            'Invalid type for parameter "date" - expecting datetime'
        )
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
    Конвертация часовой зоны в UTC-00:00

    :param hour: Час для конвертации
    :param zone: Часовой пояс в формате H

    :returns: Час в UTC-00:00 (в виде целого числа)
    """
    if zone == 0:
        # Если уже в UTC-00:00, возвращаем исходное значение часа
        return int(hour)
    else:
        new_time = hour + zone
        
        return new_time