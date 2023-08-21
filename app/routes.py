from flask import Flask, render_template, request, redirect, url_for

import os
from dotenv import load_dotenv, find_dotenv

from app import app
from app.services import maps_api, houses, planet, time_convert

load_dotenv(find_dotenv())
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        not_converted_hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        place = request.form['place']
        timezone = str(request.form['timezone'])
        
        hours = int(time_convert.time_zone_convert(hour=not_converted_hour, 
                                                   zone=timezone))
        coordinates = maps_api.get_coordinates(place)
        latitude, longitude = maps_api.extract_coordinates(coordinates)
        
        planet_positions = planet.get_planets(hours, day, month, year) 
        houses_info = []  # Список для хранения информации о домах

        house_systems = [b"B", b"Y", b"X", b"H", b"C", b"F", b"A", b"D",
                          b"N", b"G", b"I", b"i", b"K", b"U", b"M", b"P", b"T", 
                          b"O", b"L", b"Q", b"R", b"S", b"V", b"W"]
        for house_system in house_systems:
            house_info = houses.get_house(year, month, day, hours, minute, 
                                          house_system, latitude, longitude)
            house_name = houses.get_house_name(house_system)
            houses_info.append({
                "system": house_system,
                "name": house_name,
                "house_info": house_info
            })

        return render_template('result.html', planet_positions=planet_positions,
                                houses_info=houses_info)
    
    return render_template('index.html') 

@app.route('/result')
def result():
    planet_positions = request.args.get('planet_positions')  # Get planet_positions from query parameter
    
    # You can render the result page with planet_positions and display them as needed
    return render_template('result.html', planet_positions=planet_positions)
