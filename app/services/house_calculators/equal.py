# app/services/house_calculators/equal.py
import ephem

def calculate_equal_degrees(obs):
    house_degrees = []
    for house_num in range(1, 13):
        planet = ephem.Sun(obs)
        planet.compute(obs)
        cusp_longitude = calculate_equal_cusp_longitude(house_num, obs)
        planet_longitude = planet.a_ra * 180.0 / ephem.pi
        separation = planet_longitude - cusp_longitude
        if separation < 0:
            separation += 360.0
        house_degrees.append(separation)
    return house_degrees

def calculate_equal_cusp_longitude(house_num, obs):
    ascendant = ephem.Sun(obs)
    ascendant.compute(obs)
    cusp_longitude = ascendant.a_ra - (30 * (house_num - 1)) * ephem.degree
    return cusp_longitude * 180.0 / ephem.pi