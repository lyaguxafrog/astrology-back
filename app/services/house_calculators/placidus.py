# app/services/house_calculators/placidus.py
import ephem

def calculate_placidus_degrees(obs):
    house_degrees = []
    for house_num in range(1, 13):
        house_cusp = obs.sidereal_time() - (30 * (house_num - 1)) * ephem.degree
        planet = ephem.Sun(obs)
        planet.compute(obs)
        cusp_longitude = house_cusp * 180.0 / ephem.pi
        planet_longitude = planet.a_ra * 180.0 / ephem.pi
        separation = planet_longitude - cusp_longitude
        if separation < 0:
            separation += 360.0
        house_degrees.append(separation)
    return house_degrees