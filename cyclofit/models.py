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
    rides = db.relationship('Ride', backref='rider', lazy=True) #one-to-many reltn.
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
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)  
    # , nullable=False)
    # user = db.relationship('User', back_populates='profile')
    # console-print
    def __repr__(self):
        return f"User('{self.area}', '{self.contact_no}', '{self.age}', '{self.gender}', '{self.emergency_no}', '{self.date_registered}')"

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rider_weight = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    avg_speed = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    calorie_count = db.Column(db.Integer, nullable=False)
    cycle_type = db.Column(db.String(20), nullable=False)
    ride_rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.user_id}', {self.rider_weight}', '{self.duration}')"