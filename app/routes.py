from flask import Flask, render_template, request, redirect, url_for

# Дополнительные модули
import os
from dotenv import load_dotenv, find_dotenv
import swisseph as swe

# Flask-модули
from app import app
from app.services import maps_api, houses, planet, time_convert

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Установка секретного ключа для сессий
app.secret_key = os.getenv('SECRET_KEY')

# Маршрут для обработки запросов на главную страницу
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Извлечение данных из формы
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        not_converted_hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        place = request.form['place']
        timezone = str(request.form['timezone'])
        
        # Конвертация времени в соответствии с выбранным часовым поясом
        hours = int(time_convert.time_zone_convert(hour=not_converted_hour, 
                                                   zone=timezone))
        
        # Получение координат места на основе его названия
        coordinates = maps_api.get_coordinates(place)
        latitude, longitude = maps_api.extract_coordinates(coordinates)
        
        # Получение позиций планет
        planet_positions = []
        for planet_id in range(planet.swe.SUN, planet.swe.TRUE_NODE + 1):
            planet_id, planet_name, planet_position = planet.calculate_planet_position(
                hours, day, month, year, planet_id
            )
            planet_positions.append({
                "planet_id": planet_id,
                "planet_name": planet_name,
                "planet_position": planet_position
            })
        
        # Создание списка для хранения информации о домах
        houses_info = []

        # Список систем домов
        house_systems = [b"B", b"Y", b"X", b"H", b"C", b"F", b"A", b"D",
                          b"N", b"G", b"I", b"i", b"K", b"U", b"M", b"P", b"T", 
                          b"O", b"L", b"Q", b"R", b"S", b"V", b"W"]
        
        # Перебор всех систем домов
        for house_system in house_systems:
            # Получение информации о доме для текущей системы
            house_info = houses.get_house(year, month, day, hours, minute, 
                                          house_system, latitude, longitude)
            # Получение названия дома для текущей системы
            house_name = houses.get_house_name(house_system)
            
            # Добавление информации о доме в список
            houses_info.append({
                "system": house_system,
                "name": house_name,
                "house_info": house_info
            })

        # Отправка данных на страницу результата
        return render_template('result.html', planet_positions=planet_positions,
                                houses_info=houses_info)
    
    # Отображение главной страницы
    return render_template('index.html') 

# Маршрут для отображения страницы результата
@app.route('/result')
def result():
    planet_positions = request.args.get('planet_positions')  # Получение planet_positions из строки запроса
    
    # Отображение страницы результата с передачей данных
    return render_template('result.html', planet_positions=planet_positions)
