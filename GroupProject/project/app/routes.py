from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, LogoutForm, GuestForm, DeleteAccountForm, SettingsForm
from app.models import User, Post, Results
from app import apps, db
from flask_login import login_required, current_user, logout_user, login_user, UserMixin

posts = [
    {
        'author': 'Barry Allen',
        'title': 'First Event',
        'content': 'First description of event',
        'date_posted': 'April 16, 2020'
    },
    {
        'author': 'Oliver Queen',
        'title': 'Second Event',
        'content': 'Second description of event',
        'date_posted': 'April 17, 2020'
    }

]

'''This will redirect you to the route directory which is also the homepage of the application'''
@apps.route("/")
@apps.route("/home")
def home():
    return render_template('home.html', posts=posts)

'''This will redirect you to the register page where a new user can register'''
@apps.route("/register", methods=['GET', 'POST'])
def register():
    """
    Goes to Registration form in forms.py.
    Takes all methods and validators to register.html and waits for input.
    Then it waits for validation from the submit button.
    """
    if current_user.is_authenticated:
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
    return render_template('meetings.html')

'''This will redirect you to a settings page for a logged in user where the user can choose their availability'''
@apps.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    delete_account_form = DeleteAccountForm()
    settings_form = SettingsForm()
    if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first()
        user.availability_start = settings_form.availability_start.data
        user.availability_end = settings_form.availability_end.data
        user.length = settings_form.length.data
       # db.session.add(user) for new users
        db.session.commit()
        flash('availablity confirmed')
    # email_confirmation = False
    # user = User.query.filter_by(username=current_user.username).first()
    # if request.method == 'POST':
    #     user.availability_start = settings_form.availability_start.data
    #     user.availability_end = settings_form.availability_end.data
    #     user.length = int(settings_form.length.data)
    #     db.session.commit()
    #     flash("Your changes has been saved!")
    # if user.availability_start:
    #     settings_form.availability_start.data = user.availability_start
    # if user.availability_end:
    #     settings_form.availability_end.data = user.availability_end
    # if user.length:
    #     settings_form.length.data = str(user.length)
    # else:
    #     settings_form.length.data = '15'
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


@apps.route('/<username>', methods=['GET', 'POST'])
def guest(username):
    user = User.query.filter_by(username=username).first()
    # if not user and username != "guest":
    #     return "User not found", 404
    # form = GuestForm()
    # if request.method == "POST":
    #     if username != "guest" and user.availability_start:
    #         flash("Available between: " + user.availability_start + " - " + user.availability_end)
    #     else:
    #         flash("No time available.")
    results = []
    results = db.session.query(User)
    table = Results(results)
    table.border = True
    return render_template('guest.html', username=username, table=table)
    # form = form


def save_changes(user, form):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    user = User()
    user.availability_start = forms.availability_start.data
    db_session.add(album)
    db_session.commit()