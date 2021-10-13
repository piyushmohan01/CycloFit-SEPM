import json

from cyclofit import bcrypt, db
from cyclofit.models import Profile, Reward, Ride, User
from cyclofit.users.forms import (LoginForm, ProfileForm, RegistrationForm,
                                  RequestResetForm, ResetPasswordForm,
                                  UpdateGeneralForm, UpdatePersonalForm)
from cyclofit.users.utils import save_picture, send_reset_email
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

users = Blueprint('users', __name__)

@users.route('/home')
@login_required
def home():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('home.html', image_file=image_file)

@users.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('users.register02'))
    return render_template('register.html', form=form)

@users.route('/register02', methods=['GET', 'POST'])
def register02():
    form = ProfileForm()
    if form.validate_on_submit():
        if 'user_id' in session:
            session_id = session['user_id']
            user = User.query.get(session_id)
            user_profile = Profile(area=form.area.data,
                            contact_no=form.contactno.data,
                            age=form.age.data,
                            gender=form.gender.data,
                            emergency_no=form.emergencyno.data,
                            user=user)
            db.session.add(user_profile)
            db.session.commit()
            print(user_profile)
            return redirect(url_for('users.login')) # home changed to login
    return render_template('register02.html', form=form)

# checking login from database
@users.route('/login', methods=['GET', 'POST'])
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
                return redirect(next_page) if next_page else redirect(url_for('users.home'))
            flash('Login Unsuccessful! Try again!')
        else:
            flash('No Account Found!')
    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.welcome'))

@users.route("/profile")
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

# update account
@users.route("/general-update", methods=['GET', 'POST'])
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
        return redirect(url_for('users.home'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

@users.route('/personal-update', methods=['GET', 'POST'])
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
        return redirect(url_for('users.home'))
    if request.method == 'GET':
        form.area.data = user.area
        form.contactno.data = user.contact_no
        form.age.data = user.age
        form.gender.data = user.gender
        form.emergencyno.data = user.emergency_no
    return render_template('account02.html', form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email for Password Reset is sent!')
        return redirect(url_for('users.login'))
    return render_template('reset_req.html', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid/Expired Token')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password has been updated successfully!')
        return redirect(url_for('users.login'))
    return render_template('reset_tok.html', form=form)

@users.route('/ride-history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    rides = Ride.query.filter_by(user_id=current_user.id)\
                .order_by(Ride.ride_date.desc())\
                .paginate(per_page=7,page=page)
    return render_template('history.html', rides=rides)

@users.route('/stats')
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
    met = []
    calories = []
    weight_loss = []
    cycle_types = []
    ride_ratings = []

    cycle_types_dict = {
        'Afford': 0,
        'Health': 0,
        'Premium': 0,
        'Student': 0,
    }

    cycle_cal_dict = {
        'Afford': 0,
        'Health': 0,
        'Premium': 0,
        'Student': 0,
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

    ride_rating_dict = {
        '1':0,
        '2':0,
        '3':0,
        '4':0,
        '5':0,
    }

    for num in range(1,total_rides):
        ride_ids.append(num)
    for row in rides:
        ride_dates.append(row.ride_date.strftime('%a'))
        rider_weights.append(row.rider_weight)

        durations.append(row.duration*60)
        total_duration += row.duration

        avg_speeds.append(row.avg_speed)

        distances.append(row.distance)
        total_distance += row.distance

        met.append(row.met)

        calories.append(row.calorie_count)
        total_calories += row.calorie_count

        weight_loss.append(row.weight_loss)

        cycle_types.append(row.cycle_type.capitalize())

        if row.cycle_type == 'Afford':
            cycle_types_dict['Afford'] += 1
            cycle_cal_dict['Afford'] += row.calorie_count
        elif row.cycle_type == 'Health':
            cycle_types_dict['Health'] += 1
            cycle_cal_dict['Health'] += row.calorie_count
        elif row.cycle_type == 'Premium':
            cycle_types_dict['Premium'] += 1
            cycle_cal_dict['Premium'] += row.calorie_count
        elif row.cycle_type == 'Student':
            cycle_types_dict['Student'] += 1
            cycle_cal_dict['Student'] += row.calorie_count

        if row.ride_date.strftime('%a') == 'Sat':
            day_dist_dict['Sat'] += row.distance
        elif row.ride_date.strftime('%a') == 'Sun':
            day_dist_dict['Sun'] += row.distance
        elif row.ride_date.strftime('%a') == 'Mon':
            day_dist_dict['Mon'] += row.distance
        elif row.ride_date.strftime('%a') == 'Tue':
            day_dist_dict['Tue'] += row.distance
        elif row.ride_date.strftime('%a') == 'Wed':
            day_dist_dict['Wed'] += row.distance
        elif row.ride_date.strftime('%a') == 'Thu':
            day_dist_dict['Thu'] += row.distance
        elif row.ride_date.strftime('%a') == 'Fri':
            day_dist_dict['Fri'] += row.distance

        if row.ride_rating == 1:
            ride_rating_dict['1'] += 1
        if row.ride_rating == 2:
            ride_rating_dict['2'] += 1
        if row.ride_rating == 3:
            ride_rating_dict['3'] += 1
        if row.ride_rating == 4:
            ride_rating_dict['4'] += 1
        if row.ride_rating == 5:
            ride_rating_dict['5'] += 1
        # ride_ratings.append(row.ride_rating)

    cycle_types = sorted((list(set((cycle_types)))))
    cycle_types_count = list(cycle_types_dict.values())
    cycle_cal_count = list(cycle_cal_dict.values())
    ride_ratings_count = list(ride_rating_dict.values())
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
                            met=json.dumps(met),
                            calories=json.dumps(calories),
                            weight_loss=json.dumps(weight_loss),
                            cycle_types=json.dumps(cycle_types),
                            cycle_types_count=json.dumps(cycle_types_count),
                            cycle_cal_count=json.dumps(cycle_cal_count),
                            ride_ratings=json.dumps(ride_ratings),
                            ride_ratings_count=json.dumps(ride_ratings_count),
                            day_dist_count=day_dist_count)

@users.route('/Leaderboard')
def leaderboard():
    # page = request.args.get('page', 1, type=int)
    rewards = Reward.query.filter()\
        .order_by(Reward.reward_points.desc())\
        .limit(7)
    if len(list(Ride.query.filter_by(user_id=current_user.id))) == 0:
        return redirect(url_for('rides.new_ride'))
    user_list = User.query.all()
    user_count = len(list(rewards))
    return render_template('leaderboard.html', rewards=rewards, users=user_list,\
        user_count=user_count)
