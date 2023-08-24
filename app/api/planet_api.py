# Импорт необходимых библиотек и модулей
from flask import Blueprint, jsonify, request
from app.services.planet import Planets

# Создание экземпляра Blueprint для API связанного с позициями планет
planet_api = Blueprint('planet_api', __name__)

# Маршрут для получения позиций планет по POST-запросу


@planet_api.route('/planet_positions', methods=['POST'])
def get_planet_positions():
    # Получение данных из JSON-запроса
    data = request.json

    # Извлечение данных из JSON-запроса
    year = data['year']
    month = data['month']
    day = data['day']
    hours = data['hours']
    minute = data['minute']
    timezone = data['timezone']

    # Создание экземпляра класса Planets для вычисления позиций планет
    planet_calculator = Planets(year, month, day, hours, minute, timezone)
    # Получение позиций планет
    planet_positions = planet_calculator.get_planet_positions()

    # Преобразование результата в JSON и возврат
    return jsonify(planet_positions)
