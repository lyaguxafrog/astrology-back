import ephem

def calculate_planet_degrees(obs):
    planet_degrees = {}
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    for planet_name in planet_names:
        planet = getattr(ephem, planet_name)()
        planet.compute(obs)
        planet_degrees[planet_name] = planet.a_ra * 180.0 / ephem.pi
    return planet_degrees