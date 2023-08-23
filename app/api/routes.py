from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app.services import maps_api, houses, time_convert
from app.services.planet import Planets

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
api = Api(app)

class PlanetPositionsResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            year = data.get('year')
            month = data.get('month')
            day = data.get('day')
            hour = data.get('hour')
            minute = data.get('minute')
            place = data.get('place')

            house_systems = [
                b"B", b"Y", b"X", b"H", b"C", b"F", b"A", b"D",
                b"N", b"G", b"I", b"i", b"K", b"U", b"M", b"P", b"T", 
                b"O", b"L", b"Q", b"R", b"S", b"V", b"W"
            ]

            coordinates = maps_api.get_coordinates(place)
            latitude, longitude = maps_api.extract_coordinates(coordinates)

            timezone = time_convert.get_time_zone(latitude=latitude, longitude=longitude)
            converted_hour = time_convert.time_zone_convert(hour=hour, zone=timezone)

            planet_calculator = Planets(year, month, day, converted_hour, minute, timezone)
            planet_positions = planet_calculator.get_planet_positions()
        
            planet_positions_str = ",".join([f"{planet}:{position}" for planet, position in planet_positions.items()])

            houses_info = []
            for house_system in house_systems:
                house_info = houses.get_house(year, month, day, converted_hour, minute, 
                                              house_system, latitude, longitude)
                house_name = houses.get_house_name(house_system)
            
                house_info_dict = {
                    "system": house_system.decode(),
                    "name": house_name,
                    "info": house_info
                }
            
                houses_info.append(house_info_dict)

            return {
                "planet_positions": planet_positions_str,
                "houses_info": houses_info
            }

        except Exception as e:
            return {"error": str(e)}

api.add_resource(PlanetPositionsResource, '/planet_positions')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)