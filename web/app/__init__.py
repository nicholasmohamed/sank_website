from config import Config
from datetime import datetime
from dominate.tags import img
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, current_app
from flask_bootstrap import Bootstrap
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy


# Connect to database
#db = SQLAlchemy()
# set db migration
migrate = Migrate()
# add bootstrap for aesthetics
bootstrap = Bootstrap()

logo_height = "50"
logo_weight = "50"
style = "margin-top: -15px"
logo = img(src=Config.LOGO, height=logo_height, width=logo_weight, style=style)
# define menu items
topbar = Navbar(Link(logo, '/'),
                View('About', 'main.about')
                )

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)


def create_app(config_class=Config):
    # Set application
    app = Flask(__name__)
    # Get app configuration
    app.config.from_object(config_class)

    #db.init_app(app)
    #migrate.init_app(app, db)
    # Link bootstrap settings
    bootstrap.init_app(app)

    # register blueprints for different modules
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # configure navigation bar
    nav.init_app(app)

    # configure app logging
    configure_logging(app)

    return app


# Setting for python logger
def configure_logging(app):
    # create folder for logs if one does not exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # set log output
    file_handler = RotatingFileHandler('logs/' + datetime.today().strftime('%Y-%m-%d') + '_web.log',
                                       maxBytes=10240, backupCount=10)
    # set log format
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # initial log message
    app.logger.setLevel(logging.INFO)
    app.logger.info('SankBot web portal startup')

    if not app.debug and not app.testing:
        # ... configure logging setup
        print('Test')

#from app import models
