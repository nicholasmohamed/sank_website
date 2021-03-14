import os

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

    # Links for assets
    LOGO = './static/assets/Sank_Chew_Air_E_color.png'
