# app/services/time_convert.py
from datetime import datetime, timedelta
import math

def get_julian_datetime(year: int, month: int, day: int,
                         hour: int, minute: int):
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

def time_zone_convert(hour: int, zone: str) -> int:
    """
    Конвертация часовой зоны в UTC-00:00

    :param hour: Час для конвертации
    :param zone: Часовой пояс в формате UTC±HH:MM

    :returns: Час в UTC-00:00 (в виде целого числа)
    """
    if zone == 'UTC±00:00':
        return int(hour)  # Если уже в UTC-00:00, возвращаем исходное значение часа
    else:
        zone_hours = int(zone[4:6])  # Получаем часовой сдвиг
        zone_minutes = int(zone[7:9])  # Получаем минутный сдвиг
        
        input_time = datetime.strptime(str(hour), '%H')  # Создание объекта datetime
        
        time_difference = timedelta(hours=zone_hours, minutes=zone_minutes)  # Рассчет разницы времени
        
        utc_time = input_time + time_difference  # Прибавление разницы для перевода в UTC
        
        utc_hour = utc_time.strftime('%-H')  # Преобразование в строку без нуля в начале
        
        return int(utc_hour)  # Возвращаем UTC-час как целое число