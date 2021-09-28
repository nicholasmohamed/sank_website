import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Encryption key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'EisforEveryone'

    # Retrieve location of database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Set signal to application everytime database is changed
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Echo db output
    SQLALCHEMY_ECHO = True

    # Stripe settings
    YOUR_DOMAIN = 'http://127.0.0.1:5000'
    STRIPE_API_PUBLIC_KEY = os.environ.get('STRIPE_API_PUBLIC_KEY')
    STRIPE_API_SECRET_KEY = os.environ.get('STRIPE_API_SECRET_KEY')
    STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')

    # Mail settings
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    CORS_HEADERS = 'Content-Type'

    PAGE_LIST = [{"name": "PROGRAMS", "link": "main.programs"},
                 {"name": "ABOUT", "link": "main.about"},
                 {"name": "STORE", "link": "store.store"},
                 {"name": "CONTACT", "link": "main.contact"}]

    # Links for assets
    LOGO = './static/assets/Sank_Chew_Air_E_color.svg'
    STYLES = '/static/sank_home.css'