from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv, find_dotenv
import swisseph as swe
from urllib.parse import unquote_plus
from app import app
from app.services import maps_api, houses, time_convert
from app.services.planet import Planets

load_dotenv(find_dotenv())
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():

    house_systems = [b"B", b"Y", b"X", b"H", b"C", b"F", b"A", b"D",
                    b"N", b"G", b"I", b"i", b"K", b"U", b"M", b"P", b"T", 
                    b"O", b"L", b"Q", b"R", b"S", b"V", b"W"]


    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        place = request.form['place']

        coordinates = maps_api.get_coordinates(place)
        latitude, longitude = maps_api.extract_coordinates(coordinates)

        timezone = time_convert.get_time_zone(latitude=latitude, longitude=longitude)
        hours =  hour # int(time_convert.time_zone_convert(hour=not_converted_hour, zone=timezone))

        planet_calculator = Planets(year, month, day, hours, minute, timezone)
        planet_positions = planet_calculator.get_planet_positions()
        
        # planet_positions_str = ",".join([f"{planet}:{position}" for planet, position in planet_positions.items()])

        houses_info = []
        for house_system in house_systems:
            house_info = houses.get_house(year, month, day, hours, minute, 
                                          house_system, latitude, longitude)
            house_name = houses.get_house_name(house_system)
            
            house_info_dict = {
                "system": house_system.decode(),
                "name": house_name,
                "info": house_info
            }
            
            houses_info.append(house_info_dict)

        # Передаем данные в result.html
        return render_template('result.html', planet_positions=planet_positions, houses_info=houses_info)

    
    return render_template('index.html') 

@app.route('/result', methods=['GET'])
def result():
    planet_positions = request.args.get('planet_positions', '')
    houses_info = request.args.get('houses_info', '')

    planet_positions_entries = planet_positions.split(',')
    planet_positions_dict = {}
    for entry in planet_positions_entries:
        planet, position = entry.split(':')
        planet_positions_dict[planet] = position

    return render_template('result.html', planet_positions=planet_positions_dict, houses_info=houses_info)