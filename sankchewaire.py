from app import create_app
from app.models import SankMerch
from app.database import db_session as db

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(debug=True, host='0.0.0.0', port=port)

app = create_app()


# Used for creating shell context (database)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'SankMerch': SankMerch}
