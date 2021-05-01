from cyclofit import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# use same naming conventions
# pass user_id from the User Model
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# also inherting from UserMixin built-in class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False) #one-to-one reltn.
    rides = db.relationship('Ride', backref='user', lazy=True) #one-to-many reltn.
    # console-print
    def __repr__(self):
        return f"User('{self.id}',{self.username}', '{self.email}', '{self.password}' '{self.image_file}')"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(20), nullable=False)
    contact_no = db.Column(db.Integer, unique=False, nullable=False)
    age = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    emergency_no = db.Column(db.Integer, unique=False, nullable=False)
    # now = 
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # time_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow.strftime("%H:%M"))
    # day_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow.strftime('%A'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)  
    # console-print '{self.time_registered}', '{self.day_registered}'
    def __repr__(self):
        return f"User('{self.id}', '{self.area}', '{self.contact_no}', '{self.age}', '{self.gender}', '{self.emergency_no}', '{self.date_registered}', '{self.user_id}')"

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ride_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # ride_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow.strftime("%H:%M"))
    # ride_day = db.Column(db.DateTime, nullable=False, default=datetime.utcnow.strftime('%A'))
    rider_weight = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    avg_speed = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    calorie_count = db.Column(db.Integer, nullable=False)
    cycle_type = db.Column(db.String(20), nullable=False)
    ride_rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #console-print  '{self.ride_time}', '{self.ride_day}',
    def __repr__(self):
        return f"Ride('{self.id}', '{self.ride_date}', {self.rider_weight}', '{self.duration}', '{self.avg_speed}', '{self.distance}', '{self.calorie_count}', '{self.cycle_type}', '{self.ride_rating}', '{self.user_id}')"