from app.language import bp, Blueprint, g, request


@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@bp.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        abort(404)


@bp.route('/')
@bp.route('index')
def index():
    return
