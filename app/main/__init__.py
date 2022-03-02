from flask import Blueprint
import os

if os.environ.get('DEBUG_MODE') == 'true':
    bp = Blueprint('main', __name__, static_folder=os.path.join(os.getcwd(), 'app/static'))
else:
    bp = Blueprint('main', __name__, static_folder=os.path.join(os.getcwd(), '/static'))

from app.main import routes
