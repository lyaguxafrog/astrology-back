# Импорт необходимых библиотек и модулей
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from dotenv import load_dotenv, find_dotenv
import swisseph as swe
from urllib.parse import unquote_plus

# Импорт функций из различных модулей
from app import app
from app.services import maps_api, time_convert
from app.services.planet import Planets
from app.services.houses import Houses

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())
app.secret_key = os.getenv('SECRET_KEY')

# Маршрут для главной страницы


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Извлечение данных из формы
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        hours = int(request.form['hour'])
        minute = int(request.form['minute'])
        place = request.form['place']

        # Получение координат и часового пояса из места
        coordinates = maps_api.get_coordinates(place)
        latitude, longitude = maps_api.extract_coordinates(coordinates)
        timezone = time_convert.get_time_zone(latitude=latitude,
                                              longitude=longitude)

        # Создание экземпляров классов для вычислений
        planet_calculator = Planets(year, month, day, hours, minute,
                                    timezone)
        planet_positions = planet_calculator.get_planet_positions()

        house_calculator = Houses(year, month, day, hours, minute,
                                  timezone, place)
        houses_info = house_calculator.get_house()

        # Передача данных на страницу result.html
        return render_template('result.html',
                               planet_positions=planet_positions,
                               houses_info=houses_info)

    # Отображение формы на главной странице
    return render_template('index.html')

# Маршрут для страницы с результатами


@app.route('/result', methods=['GET'])
def result():
    # Получение данных из параметров запроса
    planet_positions = request.args.get('planet_positions', '')
    houses_info = request.args.get('houses_info', '')

    # Преобразование JSON-строк в списки
    planet_positions_list = json.loads(planet_positions)
    houses_info_list = json.loads(houses_info)

    # Отображение данных на странице result.html
    return render_template('result.html',
                           planet_positions=planet_positions_list,
                           houses_info=houses_info_list)
