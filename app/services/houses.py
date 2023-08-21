import swisseph as swe

from juilean_convert import get_julian_datetime


def get_house(year: int, month: int, day: int, hour: int, minute: int,
               house: bytes, latitude: float, longitude: float) -> str: 
    """
    Расчет домов во всех системах

    :params year: Год
    :params month: Месяц
    :params day: День
    :params hour: Час
    :params minute: Минута
    :params house: Система домов: https://astrorigin.com/pyswisseph/sphinx/programmers_manual/house_cusp_calculation.html
    :params latitude: Широта
    :params longitude: Долгота

    :returns: Координаты в выбранной системе домов
    """
    
    date = get_julian_datetime(year, month, day, hour, minute)
    
    house_cup = swe.houses_ex(tjdut=date, lat=latitude, lon=longitude, hsys=house, flags=0)

    return house_cup


def get_house_name(house: bytes) -> str:
    """
    Получение название Дома

    :params house: Код дома

    :returns: Название дома
    """

    house_name = swe.house_name(hsys=house)
    return house_name

