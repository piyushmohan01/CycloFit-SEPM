from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from cyclofit import db, login_manager


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
    rewards = db.relationship('Reward', backref='user', uselist=False)
    # setting token with secret key and expiration
    def get_reset_token(self, expires_sec=1800):
        serializer_token = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer_token.dumps({'user_id':self.id}).decode('utf-8')

    # static python method
    # verifying the reset token
    @staticmethod
    def verify_reset_token(token):
        serializer_token = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer_token.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # console-print
    def __repr__(self):
        return f"User('{self.id}',{self.username}', '{self.email}', '{self.image_file}')"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(20), nullable=False)
    contact_no = db.Column(db.Integer, unique=False, nullable=False)
    age = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    emergency_no = db.Column(db.Integer, unique=False, nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    # console-print
    def __repr__(self):
        return f"User('{self.id}', '{self.area}', '{self.contact_no}', '{self.age}',\
            '{self.gender}', '{self.emergency_no}', '{self.date_registered}', '{self.user_id}')"

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ride_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    duration = db.Column(db.Float, nullable=False)
    avg_speed = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    met = db.Column(db.Integer, nullable=False)
    rider_weight = db.Column(db.Integer, nullable=False)
    calorie_count = db.Column(db.Integer, nullable=False)
    weight_loss = db.Column(db.Float, nullable=False)
    cycle_type = db.Column(db.String(20), nullable=False)
    ride_rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #console-print
    def __repr__(self):
        return f"Ride('{self.id}', '{self.ride_date}', '{self.duration}', '{self.avg_speed}',\
            '{self.distance}', {self.met}', {self.rider_weight}', '{self.calorie_count}', {self.weight_loss}',\
            '{self.cycle_type}', '{self.ride_rating}', '{self.user_id}')"

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_streak = db.Column(db.Integer, nullable=False, default=0)
    cal_dur_ratio = db.Column(db.Integer, nullable=False, default=0)
    reward_points = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    # console-print
    def __repr__(self):
        return f"Reward('{self.id}', '{self.day_streak}', '{self.cal_dur_ratio}',\
            '{self.reward_points}', '{self.user_id}')"
