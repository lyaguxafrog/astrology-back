from flask import Blueprint, jsonify, request
from app.services.planet import Planets

planet_api = Blueprint('planet_api', __name__)

@planet_api.route('/planet_positions', methods=['POST'])
def get_planet_positions():
    data = request.json
    
    year = data['year']
    month = data['month']
    day = data['day']
    hours = data['hours']
    minute = data['minute']
    timezone = data['timezone']

    planet_calculator = Planets(year, month, day, hours, minute, timezone)
    planet_positions = planet_calculator.get_planet_positions()

    return jsonify(planet_positions)