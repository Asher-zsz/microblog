from app import create_app, db, cli
from app.models import User, Post


app = create_app()
cli.register(app)

@app.shell_context_processor # decorator registers the function as a shell context function. 
# When the flask shell command runs, it will invoke this function and register the items returned by it in the shell session. 
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}