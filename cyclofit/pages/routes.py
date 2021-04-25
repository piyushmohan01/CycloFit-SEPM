import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from cyclofit import app, db, bcrypt
from cyclofit.forms import RegistrationForm, ProfileForm, LoginForm, UpdateProfileForm
from cyclofit.models import User, Profile
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

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
                          age=form.age.data,
                          gender=form.gender.data,
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
            # if the user tries to access home page when logged out
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful! Try again!')
    return render_template('login.html', form=form)

@app.route('/home')
@login_required
def home():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('home.html', image_file=image_file)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route("/profile")
def profile():
    user_info = Profile.query.get(current_user.id)
    current_area = user_info.area
    current_contactno = user_info.contact_no
    current_age = user_info.age
    current_gender = user_info.gender
    current_emergencyno = user_info.emergency_no
    date_string = str(user_info.date_registered)
    date_li = list(date_string.split(' '))
    current_datereg = date_li[0]
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('profile.html', image_file=image_file,
    current_area=current_area,
    current_contactno=current_contactno,
    current_age=current_age,
    current_gender=current_gender,
    current_emergencyno=current_emergencyno,
    current_datereg=current_datereg
    )

# To update with uploaded pic
# using _ when not needed
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    folder_directory = os.path.abspath('../CycloFit/cyclofit/pages/static/profile_pics/')
    picture_path = os.path.join(app.root_path, folder_directory, picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
# update account
@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        # flash(f'Account Updated Successfully!')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)