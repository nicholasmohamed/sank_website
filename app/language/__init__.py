from flask import Blueprint

bp = Blueprint('language', __name__, url_prefix='/<lang_code>')

from app.language import routes
