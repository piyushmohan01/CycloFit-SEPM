import math
from datetime import datetime

# time_options = [15,30,45,60,90]
# time = int(input('Time: '))
# weight = int(input('Weight: '))
# speed = int(input('Speed: '))
# met = 0
# if speed == 15: met = 4
# elif speed == 20: met = 6
# elif speed == 25: met = 10
# elif speed == 30: met = 13
# elif speed == 35: met = 16
# hour = round((time/60),2)
# cal = int((hour*60*met*3.5*weight)/200)
# weight_loss = cal/7700
# distance = speed*hour
# print('Distance: {0} Km'.format(math.ceil(distance)))
# print('Calories: {0} Kcal'.format(cal))
# print('Weight Loss: {0:.2f} kg'.format(weight_loss))
print(datetime.today().strftime("%d-%b-%Y"))
print(datetime.utcnow().strftime("%d-%b-%Y"))
print(datetime.now().strftime("%d-%b-%Y"))

# Reward System :
#     dayStreak : Integer * 0.25
#     calorieDurationRatioRange : 0.25 : 0.50 : 0.75 : Total/Individual
    