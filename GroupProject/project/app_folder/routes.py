from app_folder import app
from app_folder import db
from flask import render_template, redirect
from app_folder.forms import LoginForm
from .forms import RegistrationForm
from .models import User
from flask import flash
from flask import logout_user, url_for, login

@app.route('/index')
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
        login_user(current_user) # CPI
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

@app.route('/logout', methods=['GET','POST']) #CPI
def logout():
    if not confirm_login():
        flash('You are currently not logged in!')
        return redirect(url_for('/'))
    if logout_user():
        flash('You have successfully logged out!')
        return redirect(url_for('/'))
    abort(404)
    
@app.errorhandler(404) #CPI
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.register_error_handler(404, page_not_found)




