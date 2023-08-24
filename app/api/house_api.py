# Импорт необходимых библиотек и модулей
from flask import Blueprint, jsonify, request
from app.services.houses import Houses

# Создание экземпляра Blueprint для API связанного с информацией о домах
house_api = Blueprint('house_api', __name__)

# Маршрут для получения информации о доме по POST-запросу


@house_api.route('/house_info/', methods=['POST'])
def get_house_info():
    # Получение данных из JSON-запроса
    data = request.get_json()

    # Извлечение данных из JSON-запроса
    year = data['year']
    month = data['month']
    day = data['day']
    hours = data['hours']
    minute = data['minute']
    place = data['place']
    timezone = data['timezone']

    # Создание экземпляра класса Houses для вычисления информации о домах
    house_calculator = Houses(year=year, month=month,
                              day=day, hours=hours,
                              minute=minute, timezone=timezone, place=place)
    # Получение информации о домах
    house_info = house_calculator.get_house()

    # Преобразование результата в JSON и возврат
    return jsonify(house_info)
