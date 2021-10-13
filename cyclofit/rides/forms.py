from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, RadioField
from wtforms.validators import DataRequired

class NewRideForm(FlaskForm):
    # distance and calorie-count
    duration = SelectField('Ride Duration', choices=[(15, '15 Min'), (30, '30 Min'),\
        (45, '45 Min'), (60, '1 Hour'), (90, '1.5 Hour')])
    avg_speed = SelectField('Average Speed', choices=[(15, '15 KM/H'), (20, '20 KM/H'),\
        (25, '25 KM/H'), (30, '30 KM/H'), (35, '35 KM/H')])
    rider_weight = IntegerField('Rider Weight',\
        validators=[DataRequired('Please enter your weight!')])
    cycle_type = SelectField('Cyclo-Type', choices=[('Premium', 'Cyclo-Premium'),\
        ('Health', 'Cyclo-Health'), ('Student', 'Cyclo-Student'), ('Afford', 'Cyclo-Afford')])
    ride_rating = RadioField('Ride Rating', choices=[('1','1'),('2','2'),\
        ('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Submit')
