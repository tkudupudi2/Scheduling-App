
from app_folder import app
from app_folder import db
from flask import render_template, redirect
from app_folder.forms import LoginForm
from .forms import RegistrationForm, LogoutForm, SettingsForm, GuestForm, DeleteAccountForm
from .models import User, Post
from flask import flash, url_for, request
from flask_login import logout_user, login_user, confirm_login, login_required, UserMixin
from flask_login import current_user

'''This will redirect you to the route directory which is also the homepage of the application'''
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

'''This will redirect you to the register page where a new user can register'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been succefully created!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

'''This will redirect you to the login page where authorized users will be signed in'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('meetings'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('meetings'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('meetings'))
    return render_template('login.html', title='Login', form=form)
 
'''This will redirect you to the error 404 page whenever a page is not found'''
@app.errorhandler(404) #CPI
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.register_error_handler(404, page_not_found)

'''This will redirect you to the login page when a user logs out'''
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

'''This will redirect you to the meetings page for a logged in user''''
@app.route("/meetings")
@login_required
def meetings():
    return render_template('meetings.html')

'''This will redirect you to a settings page for a logged in user where the user can choose their availability'''
@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    time = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM','10 PM']
    length = ['15 min', '30 min', '60 min']
    delete_account_form = DeleteAccountForm()
    settings_form = SettingsForm()
    email_confirmation = False
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        user.availability_start = settings_form.availability_start.data
        user.availability_end = settings_form.availability_end.data
        user.length = int(settings_form.length.data)
        db.session.commit()
        flash("Your changes has been saved!")
    if user.availability_start:
        settings_form.availability_start.data = user.availability_start
    if user.availability_end:
        settings_form.availability_end.data = user.availability_end
    if user.length:
        settings_form.length.data = str(user.length)
    else:
        settings_form.length.data = '15'
    return render_template('settings.html', delete_account_form=delete_account_form, settings_form=settings_form, email_confirmation=email_confirmation)

#@app.route("/availability", methods = ['GET', 'POST'])
#@login_required
#def add_availability():
 #   form = AvailabilityFomr()
  #  if form.validate_on_submit:
   ##    end = form.endTime.data
     #   flash('Availablity Time Updated')
      #  return redirect ("settings")
    #return render_template('availability.html', title = 'Add Availability', form = form)

'''This will redirect you to the homepage and delete the users account'''
@app.route('/deleteaccount', methods=['POST'])
def deleteaccount():
    User.query.filter_by(username=current_user.username).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for("home"))




#@app.route('/<userName>', methods=['GET', 'POST'])
#def userPage(userName) :
 #   return render_template('user.html', username = userName)  

'''This will redirect you to the users page and show their availability'''
@app.route('/<username>', methods=['GET', 'POST'])
def guest(username):
    user = User.query.filter_by(username=username).first()
    if not user and username != "guest":
        return "User not found", 404
    form = GuestForm()
    if request.method == "POST":
        if username != "guest" and user.availability_start:
            flash("Available between: " + user.availability_start + " - " + user.availability_end)
        else:
            flash("No time available.")
    return render_template('guest.html', form=form, username=username)