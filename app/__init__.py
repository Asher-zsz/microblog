from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' # to tell Flask-Login which view function handles logins, 
                           # so it can use @login_required to pretect certain views from anonymous users,
                           # when these views are accessed, the decorator will redirect users to login_view

from app import routes, models