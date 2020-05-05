from app_folder import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

'''Database for the username, email, password, and availability'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    availability_start = db.Column(db.String(64))
    availability_end = db.Column(db.String(64))
    length = db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    '''This generates a hash for the password'''
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    '''This will check the password hash'''
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    '''The username is saved'''
    def __repr__(self):
        return f'<user: {self.username}>'

'''Users have the option to upload their post which is saved into the database''''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamps = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<post: {self.body}>'

'''Provides a link to the users'''
@login.user_loader
def load_user(id):
    return User.query.get(int(id))