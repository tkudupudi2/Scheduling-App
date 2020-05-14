from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Post
from wtforms.fields.html5 import DateTimeLocalField, DateField

# Function that prompts the user to create an account
class RegistrationForm(FlaskForm):
    '''
    This class is used when the user wants to create an account
    '''
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please enter a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please enter a different email.')

# Function that prompts the user to login
class LoginForm(FlaskForm):
    '''
    This class is used whenever the user already has an account and wants to log in with it.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')

class SettingsForm(FlaskForm):
    availability_start = SelectField("Availability start:",choices=[('9 AM','9 AM'),('10 AM','10 AM'),('11 AM','11 AM'),('12 PM','12 PM'),('1 PM','1 PM'),('2 PM','2 PM'),('3 PM','3 PM'),('4 PM','4 PM'),('5 PM','5 PM'),('6 PM','6 PM'),
                                                                   ('7 PM','7 PM'),('8 PM','8 PM'),('9 PM','9 PM'),('10 PM','10 PM')])
    availability_end = SelectField("Availability end:",choices=[('9 AM','9 AM'),('10 AM','10 AM'),('11 AM','11 AM'),('12 PM','12 PM'),('1 PM','1 PM'),('2 PM','2 PM'),('3 PM','3 PM'),('4 PM','4 PM'),('5 PM','5 PM'),('6 PM','6 PM'),
                                                                   ('7 PM','7 PM'),('8 PM','8 PM'),('9 PM','9 PM'),('10 PM','10 PM')])
    length = SelectField("Length:",choices=[("15",'15 min'), ('30','30 min'), ('60','60 min')])
    entrydate = StringField('Date available')
    title = StringField('Title')
    notes = StringField('Notes')
    submit = SubmitField('Save Changes')
    email_confirmation = BooleanField('Yes')
    email_rejection = BooleanField('No')


# Function that prompts the user to logout
class LogoutForm(FlaskForm):
    '''
    This class is used when the user wants to log off from their account.
    '''
    submit = SubmitField('Logout')

class GuestForm(FlaskForm):
    date = DateField('Please pick a date: ', format='%m/%d/%y', validators=[DataRequired()])
    submit = SubmitField('Schedule appointment')