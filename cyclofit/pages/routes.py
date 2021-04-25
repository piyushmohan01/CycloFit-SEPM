from flask import render_template, url_for, flash, redirect
from cyclofit import app, db, bcrypt
from cyclofit.forms import RegistrationForm, ProfileForm, LoginForm
from cyclofit.models import User, Profile
from flask_login import login_user

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register02'))
    return render_template('register.html', form=form)

@app.route('/register02', methods=['GET', 'POST'])
def register02():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile(area=form.area.data, 
                          contact_no=form.contactno.data,
                          dob=form.dob.data,
                          emergency_no=form.emergencyno.data)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('login')) # home changed to login
    return render_template('register02.html', form=form)

# checking login from database
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if email exists and passwords match
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful! Try again!')
    return render_template('login.html', form=form)