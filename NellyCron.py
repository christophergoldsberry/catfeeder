#!/usr/bin/env python

###########################
# Import block
###########################

import datetime
from apscheduler.scheduler import Scheduler
import logging
import serial
import datetime
import twitter

###########################
# Initialize Variables
###########################

sched = Scheduler()
sched.start()
logging.basicConfig()

#Set Up API account access for @Nellysfood
consumer_key = 'DbAGiakC3vg040FJX8A7A'
consumer_secret= 'nAFnbwGi6gNb6MRUrqDamMxLSCW1A7OCF4FiepUQIWw'
access_token= '1646642456-zECt0bTkcUYQ3z5FFAjeYQbgmKLBGOX66PhiWsP'
access_token_secret= 'TxMQD7UO3miZTW4FNjcUJ77vHyVHXMraOL9n4Hx3MM'

#Initialize a twitter API instance. 
#API is the twitter object that we will use to call twitter commands
api=twitter.Api(consumer_key= consumer_key,consumer_secret=consumer_secret,access_token_key=access_token,access_token_secret=access_token_secret)


#Commented out, because will throw error
'''
device = '/dev/ttyACM0'
baud = 9600
ser = serial.Serial(device,baud)
'''

now = datetime.datetime.today()

def feedingAction(meal, debug):
	if debug is True: print "It is " + now.strftime("%c") + " and Nelly is being fed."
	api.PostUpdate(status="It is  " + now.strftime("%c") + " and Nelly is being fed.")
	#ser.write('1')
	#api.PostUpdate(status="It's currently "+datetime.datetime.today().strftime("%c")+" and I should be getting fed my "+ meal + " meal. Meow!")

feedingAction(now,True)