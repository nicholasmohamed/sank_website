from flask import Blueprint
import os

bp = Blueprint('main', __name__, static_folder=os.path.join(os.getcwd(), 'app/static'), url_prefix='/<lang_code>')

from app.main import routes
