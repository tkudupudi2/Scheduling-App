from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
import calendar
import datetime


#Creates a user database with id, username, email, and hashed password columns

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    availability_start = db.Column(db.String(64))
    availability_end = db.Column(db.String(64))
    length = db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #the user is related to the post that they post

    def __repr__(self):
        return f'<user: {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#User can upload post and it gets into the database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamps = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<post: {self.body}>'


# for guest to see appointments
class Results(Table):
    id = Col('Id', show=False)
    username = Col('User')
    email = Col('Email')
    availability_start = Col('Availability Start')
    availability_end = Col('Availability Ends')
    length = Col('Length')
   # edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))

#Provides a link to the users table since flask-login doesnt have access to database
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
