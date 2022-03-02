from flask import Blueprint
import os

bp = Blueprint('main', __name__, static_folder=os.path.join(os.getcwd(), 'app/static'))

from app.main import routes
