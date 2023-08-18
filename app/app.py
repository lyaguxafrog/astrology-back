from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
import ephem

from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location_name = request.form['location']

        geolocator = Nominatim(user_agent="astrology_app")
        location = geolocator.geocode(location_name)
        if location is None:
            error_message = "Место не найдено. Пожалуйста, введите допустимое местоположение."
            if request.accept_mimetypes.best == 'application/json':
                return jsonify({'error': error_message}), 400
            return render_template('input.html', error_message=error_message)

        obs = ephem.Observer()
        obs.lat, obs.lon = str(location.latitude), str(location.longitude)
        obs.date = f'{date} {time}'

        planet_degrees = {}
        planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
        for planet_name in planet_names:
            planet = getattr(ephem, planet_name)()
            planet.compute(obs)
            planet_degrees[planet_name] = planet.a_ra * 180.0 / ephem.pi

        house_degrees_placidus = []
        house_degrees_koch = []

        for house_num in range(1, 13):
            house_cusp = obs.sidereal_time() - (30 * (house_num - 1)) * ephem.degree
            planet = ephem.Sun(obs)
            planet.compute(obs)
            cusp_longitude = house_cusp * 180.0 / ephem.pi
            planet_longitude = planet.a_ra * 180.0 / ephem.pi
            separation = planet_longitude - cusp_longitude
            if separation < 0:
                separation += 360.0
            house_degrees_placidus.append(separation)

            planet.compute(obs)
            planet_longitude = planet.a_ra * 180.0 / ephem.pi
            separation = planet_longitude - cusp_longitude
            if separation < 0:
                separation += 360.0
            house_degrees_koch.append(separation)

        return render_template('result.html', planet_degrees=planet_degrees,
                               house_degrees_placidus=house_degrees_placidus,
                               house_degrees_koch=house_degrees_koch)
    
    return render_template('input.html')
