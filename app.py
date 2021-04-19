from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, ProfileForm, LoginForm
from datetime import datetime
app = Flask('__name__')
app.config['SECRET_KEY'] = 'fcff7fee5b3c64fc4aaf6f3b45422af2'

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for { form.username.data }', 'success')
        return redirect(url_for('register02'))
    return render_template('register.html', form=form)

@app.route('/register02', methods=['GET', 'POST'])
def register02():
    form = ProfileForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('register02.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful! Please check credentials!', 'danger')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     profile = db.relationship('Profile', backref='user', uselist=False)
#     # user_id = db.Column(db.Integer, db.ForeignKey('Profile.id'))
#     # profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
#     # uselist=False , back_populates='user'
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.password}')"

# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # emergency_no = db.Column(db.Integer, unique=True, nullable=False)
#     area = db.Column(db.String(20), nullable=False)
#     # dob = db.Column(db.String(20), nullable=False)
#     # contact_no = db.Column(db.Integer, unique=True, nullable=False)
#     date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     # parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     # profile = db.relationship('User', backref='profile_id', lazy=True)

#     def __repr__(self):
#         return f"User('{self.emergency_no}', '{self.area}', '{self.dob}', '{self.contact_no}', '{self.date_registered}')"