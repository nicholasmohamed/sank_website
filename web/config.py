import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Encryption key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'EisforEveryone'

    # Stripe API key
    API_KEY = 'sk_test_51J9ZCCBUeaWrljhjmzDSI7l72P1dbtRAW5Ro9griA0xs4Ymg3DmeDahi7M29njUANK1AYUvuAp0PxXWtapDDRgam00gzLucYR0'

    # Retrieve location of database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Set signal to application everytime database is changed
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Echo db output
    SQLALCHEMY_ECHO = True

    # Stripe settings
    YOUR_DOMAIN = 'http://127.0.0.1:5000'
    STRIPE_API_PUBLIC_KEY = 'pk_test_51J9ZCCBUeaWrljhjcNf4ePSp5fPvvJZz7byhPcmj0e4qBv99K12nJ5CZRsZXaREZVz0qCit9Mnu4H5NEi8NzTEfB00n4qY3CXN'
    STRIPE_API_SECRET_KEY = 'sk_test_51J9ZCCBUeaWrljhjmzDSI7l72P1dbtRAW5Ro9griA0xs4Ymg3DmeDahi7M29njUANK1AYUvuAp0PxXWtapDDRgam00gzLucYR0'
    STRIPE_ENDPOINT_SECRET = 'whsec_RnZjMuCPxRLGnDxIMboPeDjgSerA2Dp0'

    # Mail settings
    MAIL_USERNAME = 'test.user.sank@gmail.com'
    MAIL_PASSWORD = 'DTAWAM1test*'
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