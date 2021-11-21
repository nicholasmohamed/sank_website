from config import Config
from datetime import datetime
from dominate.tags import img
import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, current_app
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS

# Connect to database
db = SQLAlchemy()
# set db migration
migrate = Migrate()
# add bootstrap for aesthetics
bootstrap = Bootstrap()
# mail var for mailing receipts
mail = None


def create_app(config_class=Config):
    # Set application
    app = Flask(__name__)
    # Get app configuration
    app.config.from_object(config_class)

    # init database, bootstrap and mail
    db.init_app(app)
    migrate.init_app(app, db)
    # Link bootstrap settings
    bootstrap.init_app(app)
    global mail
    mail = Mail(app)

    # register blueprints for different modules
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.store import bp as store_bp
    app.register_blueprint(store_bp)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    # create database
    with app.app_context():
        db.create_all()

    # configure app logging
    configure_logging(app)

    return app


# Setting for python logger
def configure_logging(app):
    # create folder for logs if one does not exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # if online, set logging to stdout
    # set log output
    if 'DYNO' in os.environ:
        file_handler = logging.StreamHandler(sys.stdout)
    else:
        file_handler = RotatingFileHandler('logs/' + datetime.today().strftime('%Y-%m-%d') + '_web.log',
                                       maxBytes=10240, backupCount=10)

    # set log format
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger = logging.getLogger('app_logger')
    app.logger.addHandler(file_handler)

    # initial log message
    app.logger.setLevel(logging.INFO)
    app.logger.info('SankBot web portal startup')

    if not app.debug and not app.testing:
        # ... configure logging setup
        print('Test')


from app import models
