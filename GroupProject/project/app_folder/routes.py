
from app_folder import app
from app_folder import db
from flask import render_template, redirect
from app_folder.forms import LoginForm
from .forms import RegistrationForm, LogoutForm, SettingsForm
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
    #if form.validate_on_submit():
     #   pass
    #return render_template('register.html', title ='Register', form=form)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, student_courses= form.course.data) # need something like this for student column of courses
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        #return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            #return redirect('/login')
        else:
            pass
        login_user(user, remember=form.remember_me.data)

    
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

@app.route("/guest", methods=['GET'])
def guest():
    return render_template('guest.html', title='Guest')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        pass
    return render_template('settings.html', title ='Settings', form=form)
def deleteAccount():
    user = User.query.filter_by(id = current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    return render_template('index.html')




