import os
from flask import Blueprint, Flask, g

from .auxillary_bp import auxillary_bp
from .main_bp import main_bp


def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

    app.register_blueprint(auxillary_bp)
    app.register_blueprint(main_bp)

    return app
