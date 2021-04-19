from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, NumberRange
from email_validator import validate_email

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                validators=[InputRequired("Please enter your email address."), 
                Email("Enter valid email address")])
    username = StringField('Username', 
                validators=[DataRequired(), 
                Length(min=2, max=20)])
    password = PasswordField('Password',
                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                validators=[DataRequired(), 
                EqualTo('password')])
    submit = SubmitField('Register')

class ProfileForm(FlaskForm):
    emergencyno = IntegerField('Emergency Number', validators=[NumberRange(min=10), DataRequired('Enter valid number with no symbols')])
    area = StringField('Area', 
                validators=[DataRequired(), 
                Length(min=2, max=20)])
    dob = StringField('Date of Birth',
                validators=[DataRequired(), Length(min=7)])
    contactno = IntegerField('Contact Number', validators=[NumberRange(min=10), DataRequired('Enter valid number with no symbols')])
    submit = SubmitField('GO')

class LoginForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')