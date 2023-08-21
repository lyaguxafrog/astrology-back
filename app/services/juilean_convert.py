import datetime
import math

def get_julian_datetime(year: int, month: int, day: int, hour: int, minute: int):
    """
    Конвертация даты в Юлианский календарь

    :params year: Год
    :params month: Месяц      
    :params day: День
    :params hour: Час  
    :params minute: Минута

    :returns: Дату в Юлианском календаре

    """

    date = datetime.datetime(year, month, day, hour, minute, 0)

    if not isinstance(date, datetime.datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_datetime = 367 * date.year - int((7 * (date.year + int(
        (date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (
        date.hour + date.minute / 60.0 + date.second / math.pow(60,
                                                                 2)) / 24.0 - 0.5 * math.copysign(1, 100 * date.year + date.month - 190002.5) + 0.5

    return julian_datetime

