from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TimeField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from app_folder.models import User, Post
from wtforms.fields.html5 import DateTimeLocalField, DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
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

class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')

class SettingsForm(FlaskForm):
    availability_start = SelectField("Availability start:",choices=[('9 AM','9 AM'),('10 AM','10 AM'),('11 AM','11 AM'),('12 PM','12 PM'),('1 PM','1 PM'),('2 PM','2 PM'),('3 PM','3 PM'),('4 PM','4 PM'),('5 PM','5 PM'),('6 PM','6 PM'),('7 PM','7 PM'),('8 PM','8 PM'),('9 PM','9 PM'),('10 PM','10 PM')])
    availability_end = SelectField("Availability end:",choices=[('9 AM','9 AM'),('10 AM','10 AM'),('11 AM','11 AM'),('12 PM','12 PM'),('1 PM','1 PM'),('2 PM','2 PM'),('3 PM','3 PM'),('4 PM','4 PM'),('5 PM','5 PM'),('6 PM','6 PM'),('7 PM','7 PM'),('8 PM','8 PM'),('9 PM','9 PM'),('10 PM','10 PM')])
    length = SelectField("Length:",choices=[("15",'15 min'), ('30','30 min'), ('60','60 min')])
    submit = SubmitField('Save Changes')
    email_confirmation = BooleanField('Confirm Email')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')

class GuestForm(FlaskForm):
    date = DateField('Please pick a date: ', format='%m/%d/%y', validators=[DataRequired()])
    submit = SubmitField('Schedule appointment')