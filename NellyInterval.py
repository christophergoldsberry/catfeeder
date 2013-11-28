###########################
# Import block
###########################

import datetime
from apscheduler.scheduler import Scheduler
import logging
from random import choice
import serial
import datetime
from NellyFunctions import setTime, feedingAction

###########################
# Initialize Variables
###########################

sched = Scheduler()
sched.start()

#Commented out, because will throw error
'''
device = '/dev/ttyACM0'
baud = 9600
ser = serial.Serial(device,baud)
'''
logging.basicConfig()

#Real Timing Blocks. 

morningMealTime = setTime(8,30)
eveningMealTime = setTime(18,30)
midnightMealTime = setTime(23,00)


now = datetime.datetime.today()

#Test Timing Blocks
morningMealTime = setTime(now.hour, now.minute+3)
eveningMealTime = setTime(now.hour, now.minute+5)
midnightMealTime = setTime(now.hour, now.minute+7)
timeToSetNextMeals = setTime(now.hour, now.minute+9)

morningFeeding = sched.add_interval_job(feedingAction,hours=24,start_date=morningMealTime,args=['morning',True])
#eveningFeeding = sched.add_interval_job(feedingAction,hours=24,start_date=eveningMealTime,args=['evening', True])
midnightFeeding = sched.add_interval_job(feedingAction,hours=24,start_date=midnightMealTime,args=['midnight', True])
