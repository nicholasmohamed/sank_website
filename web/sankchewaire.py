from app import create_app, db
from app.models import SankMerch

app = create_app()


# Used for creating shell context (database)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'SankMerch': SankMerch}
