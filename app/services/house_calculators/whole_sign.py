# app/services/house_calculators/whole_sign.py
import ephem

def calculate_whole_sign_degrees(obs):
    house_degrees = []
    ascendant = ephem.Sun(obs)
    ascendant.compute(obs)
    ascendant_longitude = ascendant.a_ra * 180.0 / ephem.pi

    for house_num in range(1, 13):
        cusp_longitude = (ascendant_longitude + (30 * (house_num - 1))) % 360.0
        planet_longitude = ascendant.a_ra * 180.0 / ephem.pi
        separation = planet_longitude - cusp_longitude
        if separation < 0:
            separation += 360.0
        house_degrees.append(separation)
    return house_degrees