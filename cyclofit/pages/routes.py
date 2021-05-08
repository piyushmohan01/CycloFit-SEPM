import os
import secrets
import json
import math

from datetime import datetime

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from cyclofit import app, db, bcrypt, mail
from cyclofit.forms import (RegistrationForm, 
                            ProfileForm, 
                            LoginForm, 
                            UpdateGeneralForm, 
                            UpdatePersonalForm, 
                            NewRideForm, 
                            RequestResetForm, 
                            ResetPasswordForm)
from cyclofit.models import User, Profile, Ride, Reward
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

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
        session['user_id'] = user.id
        print(user.id)
        return redirect(url_for('register02'))
    return render_template('register.html', form=form)

@app.route('/register02', methods=['GET', 'POST'])
def register02():
    form = ProfileForm()
    if form.validate_on_submit():
        if 'user_id' in session:
            id = session['user_id']
            user = User.query.get(id)
            profile = Profile(area=form.area.data, 
                            contact_no=form.contactno.data,
                            age=form.age.data,
                            gender=form.gender.data,
                            emergency_no=form.emergencyno.data,
                            user=user)
            db.session.add(profile)
            db.session.commit()
            print(profile)
            return redirect(url_for('login')) # home changed to login
    return render_template('register02.html', form=form)

# checking login from database
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if email exists and passwords match
        if user:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                # if the user tries to access home page when logged out
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f'Login Unsuccessful! Try again!')
        else:
            flash(f'No Account Found!')
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
@app.route("/general-update", methods=['GET', 'POST'])
def general_update():
    form = UpdateGeneralForm()
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

@app.route('/personal-update', methods=['GET', 'POST'])
@login_required
def personal_update():
    form = UpdatePersonalForm()
    user = Profile.query.get(current_user.id)
    if form.validate_on_submit():
        user.area = form.area.data
        user.contact_no = form.contactno.data
        user.age = form.age.data
        user.gender = form.gender.data
        user.emergency_no = form.emergencyno.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.area.data = user.area
        form.contactno.data = user.contact_no
        form.age.data = user.age
        form.gender.data = user.gender
        form.emergencyno.data = user.emergency_no
    return render_template('account02.html', form=form)


@app.route('/ride-history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    rides = Ride.query.filter_by(user_id=current_user.id)\
                .order_by(Ride.ride_date.desc())\
                .paginate(per_page=7,page=page)
    return render_template('history.html', rides=rides)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='cyclofit.noreply.reset@gmail.com',
                recipients=[user.email])
    msg.body = f'''A Password-Change-Request was sent from your account.

To RESET your PASSWORD visit the Link provided and enter your NEW PASSWORD:

{url_for('reset_token', token=token, _external=True)}

Ignore if you did not make the change-request!
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'Email for Password Reset is sent!')
        return redirect(url_for('login'))
    return render_template('reset_req.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'Invalid/Expired Token')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password has been updated successfully!')
        return redirect(url_for('login'))
    return render_template('reset_tok.html', form=form)

@app.route('/stats')
@login_required
def stats():
    rides = Ride.query.filter_by(user_id=current_user.id)

    total_rides = rides.count()+1
    total_duration = 0
    total_distance = 0
    total_calories = 0
    ride_ids = []
    ride_dates = []
    rider_weights = []
    durations = []
    avg_speeds = []
    distances = []
    calories = []
    cycle_types = []
    ride_ratings = []

    cycle_types_dict = {
        'afford': 0,
        'health': 0,
        'premium': 0,
        'student': 0,
    }

    cycle_cal_dict = {
        'afford': 0,
        'health': 0,
        'premium': 0,
        'student': 0,
    }

    day_dist_dict = {
        'Sat': 0,
        'Sun': 0,
        'Mon': 0,
        'Tue': 0,
        'Wed': 0,
        'Thu': 0,
        'Fri': 0,
    }

    for num in range(1,total_rides):ride_ids.append(num)
    for row in rides:
        ride_dates.append(row.ride_date.strftime('%a'))
        rider_weights.append(row.rider_weight)

        durations.append(row.duration)
        total_duration += row.duration

        avg_speeds.append(row.avg_speed)

        distances.append(row.distance)
        total_distance += row.distance

        calories.append(row.calorie_count)
        total_calories += row.calorie_count

        cycle_types.append(row.cycle_type.capitalize())

        if row.cycle_type == 'afford': 
            cycle_types_dict['afford'] += 1
            cycle_cal_dict['afford'] += row.calorie_count
        elif row.cycle_type == 'health': 
            cycle_types_dict['health'] += 1
            cycle_cal_dict['health'] += row.calorie_count
        elif row.cycle_type == 'premium': 
            cycle_types_dict['premium'] += 1
            cycle_cal_dict['premium'] += row.calorie_count
        elif row.cycle_type == 'student': 
            cycle_types_dict['student'] += 1
            cycle_cal_dict['student'] += row.calorie_count

        if row.ride_date.strftime('%a') == 'Sat': day_dist_dict['Sat'] += row.distance
        elif row.ride_date.strftime('%a') == 'Sun': day_dist_dict['Sun'] += row.distance
        elif row.ride_date.strftime('%a') == 'Mon': day_dist_dict['Mon'] += row.distance
        elif row.ride_date.strftime('%a') == 'Tue': day_dist_dict['Tue'] += row.distance
        elif row.ride_date.strftime('%a') == 'Wed': day_dist_dict['Wed'] += row.distance
        elif row.ride_date.strftime('%a') == 'Thu': day_dist_dict['Thu'] += row.distance
        elif row.ride_date.strftime('%a') == 'Fri': day_dist_dict['Fri'] += row.distance

        ride_ratings.append(row.ride_rating)

    cycle_types = sorted((list(set((cycle_types)))))
    cycle_types_count = list(cycle_types_dict.values())
    cycle_cal_count = list(cycle_cal_dict.values())
    ride_dates = sorted((list(set((ride_dates)))))
    day_dist_count = list(day_dist_dict.values())
    print(cycle_types)
    # print(cycle_types_count)
    print(cycle_cal_count)
    # print(ratings_count)
    # print(ride_dates)
    # print(type(ride_dates))

    return render_template('stats.html',
                            total_rides=total_rides,
                            total_distance=total_distance,
                            total_duration=total_duration,
                            total_calories=total_calories,
                            ride_ids=json.dumps(ride_ids),
                            ride_dates=json.dumps(ride_dates),
                            rider_weights=json.dumps(rider_weights),
                            durations=json.dumps(durations),
                            avg_speeds=json.dumps(avg_speeds),
                            distances=json.dumps(distances),
                            calories=json.dumps(calories),
                            cycle_types=json.dumps(cycle_types),
                            cycle_types_count=json.dumps(cycle_types_count),
                            cycle_cal_count=json.dumps(cycle_cal_count),
                            ride_ratings=json.dumps(ride_ratings),
                            day_dist_count=day_dist_count)


def find_next_day(a):
    days = ['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
    for i in range(len(days)):
        if a == days[i]:
            if a == 'Fri':
                return days[0]
            else:
                return days[i+1]

def findStreak(li):
    streak = 0
    for i in range(len(li)-1):
        if li[i] != li[i+1]:
            next_day = find_next_day(li[i])
            if li[i+1] == next_day:
                streak += 1
            else:
                return -1
        else:
            streak += 0
    return streak

def findReward(rides):
    days = []
    pass_dict = {
        'streak' : 0,
        'calories' : 0,
        'duration' : 0,
        'ratio' : 0,
        'reward_pt' : 0,
    }
    print('-------------------------')
    print('Number of Rides : {0}'.format(len(list(rides))))
    for row in rides:
        days.append(row.ride_date.strftime("%a"))
        pass_dict['calories'] += row.calorie_count
        pass_dict['duration'] += row.duration
    streakCount = findStreak(days)
    if streakCount < 0:
        print('Your daily streak is broken!')
        pass_dict['streak'] = streakCount
    else:
        pass_dict['streak'] += streakCount
        print('Current Streak : {0}'.format(pass_dict['streak']))
        pass_dict['reward_pt'] += pass_dict['streak']*5
        print('Streak Reward Added (*5)')
        print('Reward After Streak : {0}'.format([pass_dict['reward_pt']]))
    print('-------------------------')
    print('Total Calories : {0}'.format(pass_dict['calories']))
    print('Total Duration : {0}'.format(pass_dict['duration']))
    pass_dict['ratio'] = math.ceil(pass_dict['calories']/pass_dict['duration'])
    print('Overall Ratio : {0}'.format(pass_dict['ratio']))
    if pass_dict['ratio'] < 250: 
        pass_dict['reward_pt'] += 1
        print('Status : Below 250 : Reward +1')
    elif pass_dict['ratio'] >= 250 and pass_dict['ratio'] < 500: 
        pass_dict['reward_pt'] += 2
        print('Status : Below 500 : Reward +2')
    if pass_dict['ratio'] >= 500 and pass_dict['ratio'] < 1000: 
        pass_dict['reward_pt'] += 3
        print('Status : Above 500 : Reward +3')
    elif pass_dict['ratio'] >= 1000: 
        pass_dict['reward_pt'] += 4
        print('Status : Above 1000 : Reward +4')
    print('Reward After Ratio : {0}'.format([pass_dict['reward_pt']]))
    print('-------------------------')
    print('Values after changes : ', end=' ')
    print(pass_dict)
    return pass_dict

@app.route('/RewardPoints')
def reward_points():
    current = Reward.query.get(current_user.id)
    if current:
        one = current.day_streak
        two = current.cal_dur_ratio
        three = current.reward_points
    else:
        one = 0
        two = 0
        three = 0
    return render_template('reward.html',
                            streak=one,
                            ratio=two,
                            reward_points=three)


def history():
    page = request.args.get('page', 1, type=int)
    rides = Ride.query.filter_by(user_id=current_user.id)\
                .order_by(Ride.ride_date.desc())\
                .paginate(per_page=7,page=page)
    return render_template('history.html', rides=rides)

@app.route('/Leaderboard')
def leaderboard():
    page = request.args.get('page', 1, type=int)
    rewards = Reward.query.filter()\
        .order_by(Reward.reward_points.desc())\
        .limit(10)
    if len(list(Ride.query.filter_by(user_id=current_user.id))) == 0:
        return redirect(url_for('new_ride'))
    users = User.query.all()
    user_count = len(users)
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('leaderboard.html', rewards=rewards, users=users, user_count=user_count)
    # , image_file=image_file)

def updateRewardRow(rides):
    user = User.query.get(current_user.id)
    current = Reward.query.get(current_user.id)
    print('Reward Row before Update : ', end=' ')
    print(current)
    print('-------------------------')
    pass_dict = findReward(rides)
    if pass_dict['streak'] < 0:
        print('Current Streak Broken!')
        current.day_streak = 0
    else:
        print('Passed Current Streak : {0}'.format(pass_dict['streak']))
        current.day_streak += pass_dict['streak']
    print('Passed Current Ratio : {0}'.format(pass_dict['ratio']))
    print('Passed Current Reward Pt : {0}'.format(pass_dict['reward_pt']))
    print('-------------------------')
    current.cal_dur_ratio = pass_dict['ratio']
    current.reward_points += pass_dict['reward_pt']
    print('Updated Current Streak : {0}'.format(current.day_streak))
    print('Updated Current Ratio : {0}'.format(current.cal_dur_ratio))
    print('Updated Current Reward Pt : {0}'.format(current.reward_points))
    print('-------------------------')
    db.session.commit()
    print('Reward Row has been updated!')
    print('-------------------------')
    one = current.day_streak
    two = current.cal_dur_ratio
    three = current.reward_points
    print('Streak : {0} | Ratio : {1} | Reward : {2}'.format(one,two,three))
    print('-------------------------')
    print('Reward Row After Update : ', end=' ')
    print(current)
    print('-------------------------')

def createRewardRow(rides): 
    user = User.query.get(current_user.id)
    print('No Reward row found!')
    print('-------------------------')
    pass_dict = findReward(rides)
    print('New Current Streak : {0}'.format(pass_dict['streak']))
    print('New Current Ratio : {0}'.format(pass_dict['ratio']))
    print('New Current Reward Pt : {0}'.format(pass_dict['reward_pt']))
    print('-------------------------')
    new_current = Reward(day_streak=pass_dict['streak'],
                        cal_dur_ratio=pass_dict['ratio'],
                        reward_points=pass_dict['reward_pt'],
                        user=user)
    print('Checking User to link with : ', end=' ')
    print(user)
    print('-------------------------')
    db.session.add(new_current)
    db.session.commit()
    print('Reward Row has been added!')
    print('-------------------------')
    one = new_current.day_streak
    two = new_current.cal_dur_ratio
    three = new_current.reward_points
    print('Streak : {0} | Ratio : {1} | Reward : {2}'.format(one,two,three))
    print('-------------------------')


def find_met(speed):
    met = 0
    if speed == 15: met = 4
    elif speed == 20: met = 6
    elif speed == 25: met = 10
    elif speed == 30: met = 13
    elif speed == 35: met = 16
    return met

@app.route('/ride/new', methods=['GET', 'POST'])
@login_required
def new_ride():
    form = NewRideForm()
    rides = Ride.query.filter_by(user_id=current_user.id)
    first_ride = True

    # if ride already exists
    if len(list(rides))!=0: 
        first_ride = False
        print('Previous Rides : ')
        for ride in rides:
            print(ride)
        print('------------------------------')

    # if no ride exists
    else: first_ride = True

    if form.validate_on_submit():
        print('------------------------------')
        user = User.query.get(current_user.id)
        duration = round(int((form.duration.data))/60,2)
        avg_speed = int(form.avg_speed.data)
        distance = math.ceil(duration*avg_speed)
        met = find_met(avg_speed)
        weight = int(form.rider_weight.data)
        calorie_count = int((duration*60*met*3.5*weight)/200)
        weight_loss = round((calorie_count/7700),2)
        print(duration)
        print(distance)
        print(met)
        print(calorie_count)
        print(weight_loss)
        print(datetime.now())
        ride = Ride(duration=duration,
                    avg_speed=form.avg_speed.data,
                    distance=distance,
                    met=met,
                    rider_weight=form.rider_weight.data,
                    calorie_count=calorie_count,
                    weight_loss=weight_loss,
                    cycle_type=form.cycle_type.data,
                    ride_rating=form.ride_rating.data,
                    user=User.query.get(current_user.id))
        db.session.add(ride)
        db.session.commit()
        print(ride)
        print('------------------------------')
        updated_rides = Ride.query.filter_by(user_id=current_user.id)
        if first_ride: 
            print('------------------------------')
            print('ADD FIRST RIDE | CREATE REWARD')
            createRewardRow(updated_rides)
        else: 
            print('------------------------------')
            print('NOT FIRST RIDE | UPDATE REWARD')
            updateRewardRow(updated_rides)
        return redirect(url_for('home'))
    return render_template('new_ride.html', form=form)
