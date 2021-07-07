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

    # Links for assets
    LOGO = './static/assets/Sank_Chew_Air_E_color.svg'
    STYLES = '/static/sank_home.css'