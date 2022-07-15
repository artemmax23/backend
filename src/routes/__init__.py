import humanfriendly as hf
import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

from .auxillary_bp import auxillary_bp
from .main_bp import main_bp


def create_app():
    app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=
                                                       hf.parse_timespan(os.getenv('ACCESS_LIFETIME', '30m')))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=
                                                        hf.parse_timespan(os.getenv('REFRESH_LIFETIME', '7d')))

    app.register_blueprint(auxillary_bp)
    app.register_blueprint(main_bp)

    jwt = JWTManager()
    jwt.init_app(app)

    return app
