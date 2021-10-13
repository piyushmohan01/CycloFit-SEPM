import datetime
import math

from cyclofit import db
from cyclofit.models import Reward, Ride, User
from cyclofit.rides.forms import NewRideForm
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

rides = Blueprint('rides', __name__)

def find_next_day(day):
    days = ['Sat','Sun','Mon','Tue','Wed','Thu','Fri']
    for i in enumerate(days):
        if day == days[i]:
            if day == 'Fri':
                return days[0]
            return days[i+1]

def find_streak(days):
    streak = 0
    print(f'LENGTH OF DAYS : {0}'.format(len(days)))
    if len(days) != 0:
        last_day = days[-1:][0]
        print('LAST DAY OF RIDE :', last_day)
        if len(days)>1:
            second_last_day = days[-2:][0]
        else:
            second_last_day = last_day
        print('SECOND LAST DAY :', second_last_day)
        if last_day != second_last_day:
            print('LAST TWO DAYS NOT EQUAL')
            next_day= find_next_day(second_last_day)
            if last_day == next_day:
                print('LAST TWO DAYS SUCCESSIVE')
                streak += 1
            elif last_day != next_day:
                print('LAST TWO DAYS NOT SUCCESSIVE')
                return -1
        elif last_day == second_last_day:
            print('LAST TWO DAYS EQUAL')
            streak += 0
    print('FINAL STREAK :', streak)
    return streak

def find_reward(ride_list):
    days = []
    pass_dict = {
        'streak' : 0,
        'calories' : 0,
        'duration' : 0,
        'ratio' : 0,
        'reward_pt' : 0,
    }
    print('-------------------------')
    print(f'Number of Rides : {0}'.format(len(list(ride_list))))
    for row in ride_list:
        days.append(row.ride_date.strftime("%a"))
        pass_dict['calories'] += row.calorie_count
        pass_dict['duration'] += row.duration
    print(days)
    streak_count = find_streak(days)
    print(streak_count)
    if streak_count < 0:
        print('Your daily streak is broken!')
        pass_dict['streak'] = streak_count
    else:
        pass_dict['streak'] += streak_count
        print(f'Current Streak : {0}'.format(pass_dict['streak']))
        pass_dict['reward_pt'] += pass_dict['streak']*5
        print('Streak Reward Added (*5)')
        print(f'Reward After Streak : {0}'.format([pass_dict['reward_pt']]))
    print('-------------------------')
    print(f'Total Calories : {0}'.format(pass_dict['calories']))
    print(f'Total Duration : {0}'.format(pass_dict['duration']))
    pass_dict['ratio'] = math.ceil(pass_dict['calories']/pass_dict['duration'])
    print(f'Overall Ratio : {0}'.format(pass_dict['ratio']))
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
    print(f'Reward After Ratio : {0}'.format([pass_dict['reward_pt']]))
    print('-------------------------')
    print('Values after changes : ', end=' ')
    print(pass_dict)
    return pass_dict

@rides.route('/RewardPoints')
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

def update_reward_row(ride_list):
    # user = User.query.get(current_user.id)
    # all_rides = Reward.query.all()
    # all_users = User.query.all()
    current = Reward.query.filter_by(user_id=current_user.id).first()
    print('*********', current)
    print('Reward Row before Update : ', end=' ')
    print(f'******** {0}'.format(current.day_streak))
    print('-------------------------')
    pass_dict = find_reward(ride_list)
    if pass_dict['streak'] < 0:
        print('Current Streak Broken!')
        current.day_streak = 0
    else:
        print(f'Passed Current Streak : {0}'.format(pass_dict['streak']))
        current.day_streak += pass_dict['streak']
    print(f'Passed Current Ratio : {0}'.format(pass_dict['ratio']))
    print(f'Passed Current Reward Pt : {0}'.format(pass_dict['reward_pt']))
    print('-------------------------')
    current.cal_dur_ratio = pass_dict['ratio']
    current.reward_points += pass_dict['reward_pt']
    print(f'Updated Current Streak : {0}'.format(current.day_streak))
    print(f'Updated Current Ratio : {0}'.format(current.cal_dur_ratio))
    print(f'Updated Current Reward Pt : {0}'.format(current.reward_points))
    print('-------------------------')
    db.session.commit()
    print('Reward Row has been updated!')
    print('-------------------------')
    one = current.day_streak
    two = current.cal_dur_ratio
    three = current.reward_points
    print(f'Streak : {0} | Ratio : {1} | Reward : {2}'.format(one,two,three))
    print('-------------------------')
    print('Reward Row After Update : ', end=' ')
    print(current)
    print('-------------------------')
    print(f'******** {0}'.format(current.day_streak))

def create_reward_row(ride_list):
    user = User.query.get(current_user.id)
    print('No Reward row found!')
    print('-------------------------')
    pass_dict = find_reward(ride_list)
    print(f'New Current Streak : {0}'.format(pass_dict['streak']))
    print(f'New Current Ratio : {0}'.format(pass_dict['ratio']))
    print(f'New Current Reward Pt : {0}'.format(pass_dict['reward_pt']))
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
    print(f'Streak : {0} | Ratio : {1} | Reward : {2}'.format(one,two,three))
    print('-------------------------')


def find_met(speed):
    met = 0
    if speed == 15:
        met = 4
    elif speed == 20:
        met = 6
    elif speed == 25:
        met = 10
    elif speed == 30:
        met = 13
    elif speed == 35:
        met = 16
    return met

@rides.route('/ride/new', methods=['GET', 'POST'])
@login_required
def new_ride():
    form = NewRideForm()
    ride_list = Ride.query.filter_by(user_id=current_user.id)
    first_ride = True

    # if ride already exists
    if len(list(ride_list))!=0:
        first_ride = False
        print('Previous Rides : ')
        for ride in ride_list:
            print(ride)
        print('------------------------------')

    # if no ride exists
    else: first_ride = True

    if form.validate_on_submit():
        print('------------------------------')
        # user = User.query.get(current_user.id)
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
        print(datetime.datetime.now())
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
            create_reward_row(updated_rides)
        else:
            print('------------------------------')
            print('NOT FIRST RIDE | UPDATE REWARD')
            print('****************ai7cg8iaogwohwvp')
            print(updated_rides)
            update_reward_row(updated_rides)
        return redirect(url_for('users.home'))
    return render_template('new_ride.html', form=form)
