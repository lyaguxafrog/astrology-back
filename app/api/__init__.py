from flask import Blueprint

# Создайте и зарегистрируйте blueprint'ы для API планет и домов
from .planet_api import planet_api
from .house_api import house_api

api_blueprint = Blueprint('api', __name__)

api_blueprint.register_blueprint(planet_api, url_prefix='/planet')
api_blueprint.register_blueprint(house_api, url_prefix='/house')