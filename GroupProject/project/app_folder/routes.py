from app_folder import app
from app_folder import db
from flask import render_template, redirect
from app_folder.forms import LoginForm
from .forms import RegistrationForm
from .models import User
from flask import flash

@app.route('/')
def home():
    myname = 'carlos' 
    mylist = ['carlos', 'jane', 'alex']
    return render_template('index.html', name=myname, names=mylist)

@app.route('/login', methods=['GET','POST'])
def login():
    form_curr = LoginForm()
    if form_curr.validate_on_submit():
        flash('Hello you logged in! Welcome to your schedule')
    return render_template('login.html', form=form_curr)
    

@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html', form=form)