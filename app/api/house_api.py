from flask import Blueprint, jsonify, request
from app.services.houses import Houses

house_api = Blueprint('house_api', __name__)

@house_api.route('/house_info/', methods=['POST'])
def get_house_info():
    data = request.get_json()

    year = data['year']
    month = data['month']
    day = data['day']
    hours = data['hours']
    minute = data['minute']
    place = data['place']
    timezone = data['timezone']

    house_calculator = Houses(year=year, month=month, day=day, hours=hours, minute=minute, timezone=timezone, place=place)
    house_info = house_calculator.get_house()

    return jsonify(house_info)




