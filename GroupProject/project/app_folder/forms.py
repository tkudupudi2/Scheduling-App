from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
#from app_folder.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')

class SettingsForm(FlaskForm):
    meetingLength = SelectField('Meeting Length: ', choices=[('60', '60 minutes', '30', '30 minutes', '15', '15 minutes')])
    emailConfirmation = BooleanField("Confirm Email")
    submit = SubmitField('Update Settings')