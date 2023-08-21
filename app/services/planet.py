import swisseph as swe

import os
from dotenv import load_dotenv, find_dotenv

swe.set_ephe_path(os.getenv('EPH_PATH'))


def get_planets(hour: int, day: int, month: int, year: int):
    """
    Получение данных о планетах по времени

    :params hour: Час
    :params day: День
    :params month: Месяц
    :params year: Год

    :returns: Список всех планет
    """
    # Вычисляем юлианскую дату в терминах эфемеридного времени (ET)
    jd_et = swe.julday(year, month, day, hour)

    # Коды планет
    planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                  swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
                  swe.MEAN_NODE, swe.TRUE_NODE]

    planet_positions = []  # Создаем список для хранения позиций планет

    # Вычисляем позиции планет и добавляем их в список
    for planet_id in planet_ids:
        planet_pos = swe.calc_ut(jd_et, planet_id)
        planet_positions.append({
            "planet_id": planet_id,
            "longitude": planet_pos[0],
            "latitude": planet_pos[1]
        })

    return planet_positions


print(get_planets(00, 12, 12, 2012))
