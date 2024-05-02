from config import Config
from datetime import datetime
from dominate.tags import img
import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, current_app, redirect, send_from_directory
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from flask_login import LoginManager, login_required, UserMixin
from app.database import init_engine, init_db, db_session

# set db migration
migrate = Migrate()
# mail var for mailing receipts
mail = None
# configure logins
login_manager = LoginManager()


def create_app(config_class=Config):
    # Set application
    app = Flask(__name__)
    # Get app configuration
    app.config.from_object(config_class)

    # init database, bootstrap and mail
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    init_db()
    migrate.init_app(app, db_session)

    global mail
    mail = Mail(app)

    # register blueprints for different modules
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/<lang_code>')

    from app.store import bp as store_bp
    app.register_blueprint(store_bp)
    # Set CORS headers
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    # configure logins
    login_manager.init_app(app)

    # set to default language
    @app.route('/')
    def index():
        return redirect(app.config['YOUR_DOMAIN'] + '/en')

    # set route for icons
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                                   'sank_tab_icon.ico', mimetype='image/png')

    login_manager.blueprint_login_views = {
        'store': '/database_login',
    }

    # create database
    # TODO remove
    # with app.app_context():
    #    db.create_all()

    # import models
    from app import models

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


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


from app import models
