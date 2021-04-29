from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, NumberRange, ValidationError
from email_validator import validate_email
from cyclofit.models import User, Profile
# , Ride
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

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

    # custom validations 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # query if the entered username is present in the db
        # if username already present throw validation error
        if user:
            raise ValidationError('Username already taken! Pick another!')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # query if the entered email is present in the db
        # if email already present throw validation error
        if user:
            raise ValidationError('Email already taken! Pick another!')

class ProfileForm(FlaskForm):
    area = StringField('Area', 
                validators=[DataRequired(), 
                Length(min=2, max=20)])
    contactno = IntegerField('Contact Number', validators=[NumberRange(min=10), DataRequired('Enter valid number with no symbols')])
    age = StringField('Age',
                validators=[DataRequired()])
    # gender = StringField('Gender',
    #             validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female')], validators=[DataRequired()])
    emergencyno = IntegerField('Emergency Number', validators=[NumberRange(min=10), DataRequired('Enter valid number with no symbols')])
    submit = SubmitField('GO')

class LoginForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateGeneralForm(FlaskForm):
    email = StringField('Email',
                validators=[InputRequired("Please enter your email address."), 
                Email("Enter valid email address")])
    username = StringField('Username', 
                validators=[DataRequired(), 
                Length(min=2, max=20)])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # custom validations 
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            # query if the entered username is present in the db
            # if username already present throw validation error
            if user:
                raise ValidationError('Username already taken! Pick another!')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # query if the entered email is present in the db
            # if email already present throw validation error
            if user:
                raise ValidationError('Email already taken! Pick another!')
            
class UpdatePersonalForm(FlaskForm):
    area = StringField('Area', 
                validators=[DataRequired(), 
                Length(min=2, max=20)])
    contactno = IntegerField('Contact Number', validators=[NumberRange(min=10), DataRequired('Enter valid number with no symbols')])
    age = StringField('Age',
                validators=[DataRequired()])
    # gender = StringField('Gender',
    #             validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female')], validators=[DataRequired()])
    emergencyno = IntegerField('Emergency Number', validators=[NumberRange(min=10), DataRequired('Enter valid number with no symbols')])
    submit = SubmitField('Update')
    
class NewRideForm(FlaskForm):
    # distance and calorie-count
    duration = SelectField(u'Ride Duration', choices=[('15', '15 min'), ('30', '30 min'), ('45', '45 min'), ('60', '60 min')])
    avg_speed = SelectField(u'Average Speed', choices=[('10', '10 KMPH'), ('20', '20 KMPH'), ('30', '30 KMPH'), ('40', '40 KMPH')])
    rider_weight = IntegerField('Rider Weight', validators=[DataRequired('Please enter your weight!')])
    cycle_type = SelectField(u'Cyclo-Type', choices=[('premium', 'Cyclo-Premium'), ('health', 'Cyclo-Health'), ('student', 'Cyclo-Student'), ('afford', 'Cyclo-Afford')])
    ride_rating = RadioField('Ride Rating', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Submit')

    # gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female')], validators=[DataRequired()])
