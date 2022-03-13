from flask import Blueprint

bp = Blueprint('store', __name__, url_prefix='/<lang_code>')

from app.store import routes