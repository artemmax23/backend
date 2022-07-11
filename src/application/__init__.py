from .auxillary import auxillary
from .main import main
from flask import Blueprint, Flask, g
import os

def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

    app.register_blueprint(auxillary)
    app.register_blueprint(main)

    return app