from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

apps = Flask(__name__)
apps.config.from_object(Config)

login = LoginManager(apps)
login.login_view = 'login'

db = SQLAlchemy(apps)
from app import routes, models
db.create_all()