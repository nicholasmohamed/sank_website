from flask import Blueprint
import os

bp = Blueprint('foamwars', __name__, static_folder=os.path.join(os.getcwd(), 'app/static'))

from app.foamwars import routes
