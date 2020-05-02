
from app_folder import app
from app_folder import db
from flask import render_template, redirect
from app_folder.forms import LoginForm
from .forms import RegistrationForm, LogoutForm
from .models import User
from flask import flash, url_for
from flask_login import logout_user, login_user, confirm_login
from flask_login import current_user

@app.route('/')
def home():
    myname = 'carlos' 
    mylist = ['carlos', 'jane', 'alex']
    return render_template('index.html', name=myname, names=mylist)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', title ='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       pass
    return render_template('login.html', title ='Login', form=form)

# route for logout
#@app.route('/logout', methods=['GET', 'POST']) #CPI
#def logout():
 #   if not confirm_login():
  #      flash('You are currently not logged in!')
   #     return redirect('/')
    #if logout_user():
     #   flash('You have successfully logged out!')
      #  return redirect('/')
    #abort(404)
  
@app.errorhandler(404) #CPI
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.register_error_handler(404, page_not_found)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
       pass
    return render_template('logout.html', title ='Login', form=form)



