from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, LogoutForm, GuestForm, DeleteAccountForm, SettingsForm
from app.models import User, Post, Results, Schedule
from app import apps, db
from flask_login import login_required, current_user, logout_user, login_user, UserMixin

'''This will redirect you to the route directory which is also the homepage of the application'''
@apps.route("/")
@apps.route("/home")
def home():
    return render_template('home.html')

'''This will redirect you to the register page where a new user can register'''
@apps.route("/register", methods=['GET', 'POST'])
def register():
    """
    Goes to Registration form in forms.py.
    Takes all methods and validators to register.html and waits for input.
    Then it waits for validation from the submit button.
    """
    if current_user.is_authenticated:
        flash("You are currently logged in")
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

'''This will redirect you to the login page where authorized users will be signed in'''
@apps.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login page
    Realistically, if you have registered already, you go here.
    Takes all methods and validators to login.html and waits for input.
    Then it waits for validation from the submit button.
    """
    if current_user.is_authenticated:
        flash("User is authenticated")
        return redirect(url_for('meetings'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('meetings'))
    return render_template('login.html', title='Login', form=form)

'''This will redirect you to the error 404 page whenever a page is not found'''
# @app.errorhandler(404) #CPI
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404


@apps.route('/meetings')
@login_required
def meetings():
    user = User.query.filter_by(username=current_user.id).first()
    user_schedule = Schedule(owner=user)
    results = []
    results = db.session.query(Schedule).filter_by(user_id=current_user.id)
    table = Results(results)
    table.border = True
    return render_template('meetings.html',table=table)

'''This will redirect you to a settings page for a logged in user where the user can choose their availability'''
@apps.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    delete_account_form = DeleteAccountForm()
    settings_form = SettingsForm()
    if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first()
        open_date = Schedule(owner=user)
        open_date.availability_start = settings_form.availability_start.data
        open_date.availability_end = settings_form.availability_end.data
        open_date.length = settings_form.length.data
        open_date.entrydate = settings_form.entrydate.data
       # db.session.add(user) for new users
        db.session.commit()
        flash('Availablity added')
    return render_template('settings.html', delete_account_form=delete_account_form, settings_form=settings_form)
    #email_confirmation=email_confirmation


@apps.route('/deleteaccount', methods=['POST'])
def deleteaccount():
    User.query.filter_by(username=current_user.username).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for("home"))


@apps.route('/logout')
@login_required
def logout():
    """
    Logout form
    Currently does nothing and cannot be accessed
    Clicking would log out account
    Its here for the future
    """
    logout_user()
    return redirect(url_for('login'))

# guests will be able to see the users schedule
@apps.route('/<username>', methods=['GET', 'POST'])
def guest(username):
    user = User.query.filter_by(username=username).first()
    user_schedule = Schedule(owner=user)
    results = []
    results = db.session.query(Schedule).filter_by(user_id=user.id)
    table = Results(results)
    table.border = True
    return render_template('guest.html', username=username, table=table)
    # form = form


#for when guests click on the schedule
@apps.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    #user = User.query.filter_by(id=id).first()
    
    user = User.query.get(id)
    user_schedule = Schedule(owner=user)
    settings_form = SettingsForm()
    results = []
    results = db.session.query(Schedule).filter_by(id=id) 
    table = Results(results)
    table.border = True
    if request.method == 'POST':
        user_schedule.title = settings_form.title.data
        user_schedule.notes = settings_form.notes.data
        db.session.commit()
        flash('Discription added')
    return render_template('edit_schedule.html', id=id, table=table,
                            settings_form=settings_form)
