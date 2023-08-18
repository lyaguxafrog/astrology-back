from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
import ephem

from app import app

from app.services.planet_calculator import calculate_planet_degrees
from app.services.house_calculators import (
    placidus, koch, equal, porphyry, regiomontanus, campanus, whole_sign
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location_name = request.form['location']

        geolocator = Nominatim(user_agent="astrology_app")
        location = geolocator.geocode(location_name)

        if not location:
            error_message = "Место не найдено. Пожалуйста, введите допустимое местоположение."
            return render_template('input.html', error_message=error_message)

        obs = ephem.Observer()
        obs.lat, obs.lon = str(location.latitude), str(location.longitude)
        obs.date = f'{date} {time}'

        planet_degrees = calculate_planet_degrees(obs)

        house_systems = [
            ('Placidus', placidus.calculate_placidus_degrees),
            ('Koch', koch.calculate_koch_degrees),
            ('Equal', equal.calculate_equal_degrees),
            ('Porphyry', porphyry.calculate_porphyry_degrees),
            ('Regiomontanus', regiomontanus.calculate_regiomontanus_degrees),
            ('Campanus', campanus.calculate_campanus_degrees),
            ('Whole Sign', whole_sign.calculate_whole_sign_degrees)
        ]

        house_degrees = {system_name: calculate_fn(obs) for system_name, calculate_fn in house_systems}

        return render_template('result.html', planet_degrees=planet_degrees, house_degrees=house_degrees)
    
    return render_template('input.html')

