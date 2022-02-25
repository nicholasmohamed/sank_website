import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

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
    YOUR_DOMAIN = os.environ.get('WEBSITE_DOMAIN')
    STRIPE_API_PUBLIC_KEY = os.environ.get('STRIPE_API_PUBLIC_KEY')
    STRIPE_API_SECRET_KEY = os.environ.get('STRIPE_API_SECRET_KEY')
    STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')
    STRIPE_PROVINCIAL_TAX = os.environ.get('STRIPE_PROVINCIAL_TAX')
    STRIPE_FEDERAL_TAX = os.environ.get('STRIPE_FEDERAL_TAX')
    STRIPE_SHIPPING_RATE_1 = os.environ.get('STRIPE_SHIPPING_RATE_1')
    STRIPE_SHIPPING_RATE_2 = os.environ.get('STRIPE_SHIPPING_RATE_2')

    # Mail settings
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    CORS_HEADERS = 'Content-Type'

    # Database password
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'CultureIsEverything'
    DATABASE_PASSWORD_HASH = generate_password_hash(DATABASE_PASSWORD)

    PAGE_LIST = [{"name": "about", "link": "main.about"},
                 {"name": "shop", "link": "store.store"}]#,
                # {"name": "contact", "link": "main.contact"}]