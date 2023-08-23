# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_restful import Api
from .api import api_bp

from app.api import routes

app = Flask(__name__)
bootstrap = Bootstrap(app)
api = Api(app)  # Инициализация Flask-RESTful

app.register_blueprint(api_bp, url_prefix='/app')

from app import routes, author