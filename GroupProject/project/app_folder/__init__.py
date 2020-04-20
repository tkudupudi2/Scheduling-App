from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager #CPI

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app) #CPI

db = SQLAlchemy(app)

from app_folder import routes, models