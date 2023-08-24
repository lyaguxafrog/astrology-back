#/app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

from app import routes, author

from app.api import api_blueprint

app.register_blueprint(api_blueprint, url_prefix='/api')