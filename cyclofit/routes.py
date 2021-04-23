from flask import render_template, url_for, flash, redirect
from cyclofit import app
from cyclofit.forms import RegistrationForm, ProfileForm, LoginForm
from cyclofit.models import User, Profile

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