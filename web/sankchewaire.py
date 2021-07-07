from app import create_app

app = create_app()


# Used for creating shell context (database)
'''
@app.shell_context_processors
def make_shell_context():
    return {'db': db, 'SankMerchDb': SankMerchDb}
'''
