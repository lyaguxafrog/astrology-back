from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
import ephem

from app import app

from app.services.planet_calculator import calculate_planet_degrees
from app.services.house_calculators import placidus, koch, equal, porphyry, regiomontanus, campanus, whole_sign

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
            return render_template('input.html', error_message=error_message)

        obs = ephem.Observer()
        obs.lat, obs.lon = str(location.latitude), str(location.longitude)
        obs.date = f'{date} {time}'

        planet_degrees = calculate_planet_degrees(obs)

        house_degrees_placidus = placidus.calculate_placidus_degrees(obs)
        house_degrees_koch = koch.calculate_koch_degrees(obs)
        house_degrees_equal = equal.calculate_equal_degrees(obs)
        house_degrees_porphyry = porphyry.calculate_porphyry_degrees(obs)
        house_degrees_regiomontanus = regiomontanus.calculate_regiomontanus_degrees(obs)
        house_degrees_campanus = campanus.calculate_campanus_degrees(obs)
        house_degrees_whole_sign = whole_sign.calculate_whole_sign_degrees(obs)

        return render_template('result.html', planet_degrees=planet_degrees,
                               house_degrees_placidus=house_degrees_placidus,
                               house_degrees_koch=house_degrees_koch,
                               house_degrees_equal=house_degrees_equal,
                               house_degrees_porphyry=house_degrees_porphyry,
                               house_degrees_regiomontanus=house_degrees_regiomontanus,
                               house_degrees_campanus=house_degrees_campanus,
                               house_degrees_whole_sign=house_degrees_whole_sign
                               )
    
    return render_template('input.html')

if __name__ == '__main__':
    app.run(debug=True)
