from flask import Flask
from .router import routes

def create_app():
    app = Flask(__name__)
    routes(app)
    return app