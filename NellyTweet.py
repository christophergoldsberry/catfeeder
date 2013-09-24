#!/usr/bin/env python

#This program sets up a feeding schedule for Nelly, and feeds her each day
#according to the schedule established.  Changes to the schedule (additions), 
#or evening meals (if we're out), or treats are handled by sending tweets to the
#nelly twitter account (@NellysFood)

#Import Libraries 

import twitter
import datetime
"""I looked at doing this three different ways before I settled on the one I thought worked best.
They're commented out, but feel free to explore."""
#from datetime import datetime
#from threading import Timer
#from crontab import CronTab
from apscheduler.scheduler import Scheduler
import logging
from random import choice

logging.basicConfig()

#--------------------
#---Variables--------
#--------------------

#setup a scheduler object
sched = Scheduler()
sched.start()


#Set Up API account access for @Nellysfood
consumer_key = 'DbAGiakC3vg040FJX8A7A'
consumer_secret= 'nAFnbwGi6gNb6MRUrqDamMxLSCW1A7OCF4FiepUQIWw'
access_token= '1646642456-zECt0bTkcUYQ3z5FFAjeYQbgmKLBGOX66PhiWsP'
access_token_secret= 'TxMQD7UO3miZTW4FNjcUJ77vHyVHXMraOL9n4Hx3MM'

#Initialize a twitter API instance. 
#API is the twitter object that we will use to call twitter commands
api=twitter.Api(consumer_key= consumer_key,consumer_secret=consumer_secret,access_token_key=access_token,access_token_secret=access_token_secret)

#Set up initial meal schedules, roll feedings over to next day if time has already passed today
morningMealTime = datetime.datetime.today() + datetime.timedelta(minutes = 3)
eveningMealTime = datetime.datetime.today()  + datetime.timedelta(minutes = 8)
midnightMealTime = datetime.datetime.today()  + datetime.timedelta(minutes = 12)
timeToSetNextMeals = datetime.datetime.today()  + datetime.timedelta(minutes = 17)


'''ACTUAL BLOCK BELOW, REPLACE AFTER DEBUGGING DONE
#Set up initial meal schedules, roll feedings over to next day if time has already passed today
morningMealTime = datetime.datetime.today().replace(hour=10,minute=03)
#if (morningMealTime - datetime.datetime.today()).total_seconds() < 0:
#	morningMealTime = morningMealTime.replace(day=morningMealTime.day+1)
eveningMealTime = datetime.datetime.today().replace(hour=10,minute=05)
#if (eveningMealTime - datetime.datetime.today()).total_seconds() < 0:
#	eveningMealTime = eveningMealTime.replace(day=eveningMealTime.day+1)
midnightMealTime = datetime.datetime.today().replace(hour=10,minute=07)
#if (midnightMealTime - datetime.datetime.today()).total_seconds() < 0:
#	midnightMealTime = midnightMealTime.replace(day=midnightMealTime.day+1)


timeToSetNextMeals = datetime.datetime.today().replace(hour=23,minute=59)
'''

# Each tweet has a unique id, which is constantly incrementing; this will get updated each time
# a tweet is read so we never duplicate an action requested by a tweet.
# it initalizes at one (THE BEGINNING OF TIIIIME)
lastTwitterStatusID = 1

#only tweets from allowed users are parsed.  This is the user id array of allowed users.  Currently @goldsberry only.
allowedUsers= [14875882]

#boolean for whether someone's already given the cat a treat
treatsAlreadyGivenToday = False

#boolean for whether or not an evening meal has been requested
eveningFeedRequested = True

#Debug toggle adds print actions
debug = True

#twitter dictionary key/value pairs
tweet = {}

#-----------------------
#---Function Blocks
#-----------------------


# Called by SearchForTweets. 
# Determines whether the user is allowed to command Nelly's food bowl and returns True or False
def isAllowedUser(requestMaker):
	if debug is True: print "checking if allowed user"
	for user in allowedUsers:
		if user == requestMaker:
			return True
	return False


#Called by Search for Tweets
#Strips the first hashtag in the tweet and returns it as a command and returns the hashtag word minus the '#'
def parseCommandWord(command):
	if debug is True: print "now parsing command word"
	for word in command.split():
		if word.startswith("#"):
				requestedAction = word.strip("#")
				"""right now, this only returns the first hashtag in the tweet.  
				In the future, we could use .extend() to add more keywords to the list, and then use
				something like 'for COMMAND in REQUESTEDACTION:' etc etc. """
				return requestedAction.lower()
#The following is commented out for now.

def updateMealTime(tweet):
	api.PostUpdate(status="This feature is coming soon!",in_reply_to_status_id=tweet["statusID"])


"""#updates either the morning, evening, or midnight feeding time.
def updateCorrectMealTimer(mealTimeToUpdate, newMealTime):
	global morningMeal,
	if debug is True: print "now determining correct meal"
	if mealTimeToUpdate == morningMeal:
		if debug is True: print "morning"
		morningMealTimer.cancel()
		morningMeal.replace(hour = newMealTime.hour, minute= newMealTime.minute)
		timeleft = morningMeal  - datetime.datetime.today()
		morningMealTimer = Timer(timeleft.total_seconds(), feedingAction)
		morningMealTimer.start()
	elif mealTimeToUpdate == eveningMeal:
		if debug is True: print "evening"
		try:
			eveningMealTimer.cancel()
			eveningMeal.replace(hour = newMealTime.hour, minute= newMealTime.minute)
			if eveningMealScheduled is True: #it's not nessecarily the case that we have an active feeding scheduled for the evening.  if so, we reset the timer.
				timeleft = eveningMeal  - datetime.datetime.today()
				eveningMealTimer = Timer(timeleft.total_seconds(), feedingAction)
				eveningMealTimer.start()
		except NameError:
			print "no evening meal scheduled!"
	elif mealTimeToUpdate == midnightMeal:
		if debug is True: print "midnight"
		midnightMealTimer.cancel()
		midnightMeal.replace(hour = newMealTime.hour, minute= newMealTime.minute)
		timeleft = midnightMeal  - datetime.datetime.today()
		midnightMealTimer = Timer(timeleft.total_seconds(),feedingAction)
		midnightMealTimer.start()
	else:
		print mealTimeToUpdate + "is not updateable, because it not a meal keyword!"


# Called by updateCorrectMealTimer
# takes the twitter text, searches for a STRPtime-able word, and sets it as the new meal time
def parseNewMealTimeFromTweet(text): 
	if debug is True: print "finding new mealtime"
	for word in text.split():
		if debug is True: print "now trying "+word
		#Try to strip each word, in series into a datetime.  Tweets will be written in #:##AM/PM format.
		try:
			newMealTime = datetime.datetime.strptime(word,"%I:%M%p")
			return newMealTime
		except ValueError:
			print "not a strippable object, moving on to next"

#takes the twitter text, searches for a STRPtime-able word, and sets it as the new meal
def getCorrectMealFromTweet(tweet): 
	text = tweet[text]
	if debug is True: print "now finding correct scheduled meal to replace (morn/evening/midnight)"
	for word in text.split():
		#Look for either morning, evening, or midnight as keyword in the tweet text
		if word.lower() == 'morning':
			return morningMeal
		elif word.lower() == 'evening':
			return eveningMeal
		elif word.lower() == 'midnight':
			return midnightMeal
		else:
			api.PostUpdate(status="Try again, and include either 'morning', 'evening', or 'midnight' in your tweet text, followed by the new (military) time in HH:MM.", in_reply_to_status_id=tweet['statusID'])
			return morningMeal

def updateMealTime(tweet):
	mealTimeToUpdate = getCorrectMealFromTweet(text[fullText])
	newMealTime = parseNewMealTimeFromTweet(tweet[fullText])
	updateCorrectMealTimer(mealTimeToUpdate,newMealTime)

"""

#Searches for tweets, and executes a command
def searchForTweets():
	global lastTwitterStatusID, debug, tweet
	#print str(datetime.now().hour) + ":" + str(datetime.now().minute)
	if debug is True: print "searching for tweets!"
	newMentions = api.GetMentions(since_id=str(lastTwitterStatusID)) #calls for mentions greater than last recorded mention
	try: 
		mention = newMentions.pop(0)
		if mention.id > lastTwitterStatusID & isAllowedUser(mention.user.id):
			lastTwitterStatusID = mention.id
			user = mention.user.id
			username = mention.user.name
			command = parseCommandWord(mention.text)
			print "saving pieces of tweet to memory"
			fullText = mention.text
			statusID = mention.id
			tweet['statusID']=statusID
			tweet['fullText'] = fullText
			tweet['command']= command
			tweet['user']= user
			tweet['username']= username
		#determine what kind of command has been made
			if command in controlOptions:
				controlOptions[command](tweet)
			else: api.PostUpdate(status = nellySpeak('noCommandFound',tweet),in_reply_to_status_id = tweet['statusID'])
		else: api.PostUpdate(status= "You aren't on my allowed users list! Talk to @goldsberry to get access!", in_reply_to_status_id = tweet['statusID'])
	except IndexError:
		print "No New Mentions. Will re-call in 1 minute."
	#mention.id if statement will fail silently if no new mentions exist
	#if (mention[0].text).find('test'):
	#if (mention[0].user.name) == 'goldsberry':
		#print "this came from golds"
	#print str(datetime.now().hour) + ":" + str(datetime.now().minute)



#reset everything for tomorrow
def setTomorrowsMeals():
	global morningMealTime, eveningMealTime,midnightMealTime,timeToSetNextMeals
	#nextMorningMeal = morningMeal.replace(day=morningMeal.day+1)
	#nextEveningMeal = eveningMeal.replace(day=eveningMeal.day+1)
	#nextMidnightMeal = midnightMeal.replace(day=midnightMeal.day+1)
	#timeToSetNextMeals = timeToSetNextMeals.replace(day=timeToSetNextMeals.day+1)
	if debug is True: print "setting tomorrow's meals"
	morningMealTime = morningMealTime + datetime.timedelta(minutes = 5)
	eveningMealTime = eveningMealTime + datetime.timedelta(minutes = 5)
	midnightMealTime = midnightMealTime + datetime.timedelta(minutes = 5)
	timeToSetNextMeals = timeToSetNextMeals + datetime.timedelta(minutes = 5)
	print "Morning: " + morningMealTime.strftime("%c")
	print "Evening: " + eveningMealTime.strftime("%c")
	print "Midnight: " + midnightMealTime.strftime("%c")
	print "Reset: " + timeToSetNextMeals.strftime("%c")

	if debug is True:
		if treatsAlreadyGivenToday is False:
			print "no treats given today"
		else: print "treats given today"

	morningFeed = sched.add_date_job(feedingAction,morningMealTime,['morning'])
	eveningFeed = sched.add_date_job(eveningFeedingAction,eveningMealTime)
	midnightFeed = sched.add_date_job(feedingAction,midnightMealTime,['midnight'])
	setNextDayMealTimes = sched.add_date_job(setTomorrowsMeals,timeToSetNextMeals)



def feedingAction(meal):
	if debug is True: print meal + " called."
	api.PostUpdate(status="It's currently "+datetime.datetime.today().strftime("%c")+" and I should be getting fed my "+ meal + " meal. Meow!")


# Called every night.  If the "eveningMealRequested" boolean has been set to true, it performs a feeding. If not, it doesn't.
def eveningFeedingAction():
	global eveningFeedRequested
	if debug is True: print "Evening Meal Called"
	if eveningFeedRequested is True:
		api.PostUpdate(status="It's currently "+datetime.datetime.today().strftime("%c")+" and I am being fed my evening meal")
		eveningFeedRequested = False
	else:
		api.PostUpdate(status="It's currently "+ datetime.datetime.today().strftime("%c")+ " but no evening feeding requested")

def addEveningMeal(tweet):
	global eveningFeedRequested
	if debug is True: print "eveningMealRequested"
	eveningFeedRequested = True
	
def giveTreat(tweet):
	global treatsAlreadyGivenToday
	if debug is True: print "treat detected"
	if treatsAlreadyGivenToday is False: 
		api.PostUpdate(status=nellySpeak('giveTreat',tweet),in_reply_to_status_id=tweet['statusID'])
		treatsAlreadyGivenToday = True
	else:
		api.PostUpdate(status = nellySpeak('noTreat',tweet),in_reply_to_status_id = tweet['statusID'])

def updateLastTweetID():
	lastMention = api.GetMentions(since_id=str(1)).pop(0)
	return lastMention.id

def nellySpeak(kindOfAction,tweet):
	if kindOfAction == 'giveTreat':
		potentialResponses=[
		"Thanks for the treat "+tweet['username']+"!",
		"OH GOD YOU'RE MY FAVORITE PERSON EVERRRRR OH ILOVEYOUILOVEYOUILOVEYOUUUU."
		"@Goldsberry never gives me treats. I like you better",
		"If "+tweet['username']+" wants me to move to their house, I probably would. If I felt like it.",
		"OH GOD MOAR PLEEZ",
		"[the sounds of Nelly eating way to goddamn fast]"
		]
	elif kindOfAction == 'noTreat':
		potentialResponses=[
			"You're too late, "+tweet['username']+"! I already got a treat today!",
			"If you're trying to fatten me up, someone else already beat you to it.  Quick, break in to Chris's house and feed me manually",
			"There's this stupid rule that I can only have one treat per day. I'm starving!",
			"MEW MEW MEW MEW MEWMEW MEWMEWMEWMEW MEWWWWWWW"
		]
	elif kindOfAction == 'noCommandFound':
		potentialResponses= [
			"ENGLISH, "+tweet['username']+". DO YOU SPEAK IT?  Uh, I mean, 'Meow'? (I respond to #updateMealtime, #giveTreat, and #addEveningMeal)",
			"I don't understand a word you're saying. FEED ME. (I respond to #updateMealtime, #giveTreat, and #addEveningMeal)",
			"WTF. (I respond to #updateMealtime, #giveTreat, and #addEveningMeal)",
			"MEW MEW MEW MEWWWWWW (I respond to #updateMealtime, #giveTreat, and #addEveningMeal)",
			"Try again, "+tweet['username']+". You give me food, and I don't murder you in your sleep. Deal? (Try #updateMealtime, #giveTreat, or #addEveningMeal)",
			"Someday, I will murder the dog that lives downstairs. (Try #updateMealtime, #giveTreat, or #addEveningMeal)",
			"Did you know? I secretly loathe string. (Try #updateMealtime, #giveTreat, or #addEveningMeal)",
			"I'm just going to sit here and lick my butt 'till you get your shit together. (Try #updateMealtime, #giveTreat, or #addEveningMeal)",
			"It's currently "+datetime.datetime.today().strftime("%c")+" and "+tweet['username']+" still doesn't have their shit together."
		]
	else: potentialResponses = ["Help! I don't know what's going on! I'm probably trapped in the laundry room!"]
	return choice(potentialResponses)


#Function Dictionary
controlOptions = {'updatemealtime' : updateMealTime,
				  'addeveningmeal' : addEveningMeal,
				  'givetreat' : giveTreat
}

#tweetSearch= Timer(60,searchForTweets)
#tweetSearch.start()

#setNextMeals()

#morningMealTimer = Tim
if datetime.datetime.today() < morningMealTime: morningFeed = sched.add_date_job(feedingAction,morningMealTime,['morning'])
if datetime.datetime.today() < eveningMealTime: eveningFeed = sched.add_date_job(eveningFeedingAction,eveningMealTime)
if datetime.datetime.today() < midnightMealTime: midnightFeed = sched.add_date_job(feedingAction,midnightMealTime,['midnight'])
if datetime.datetime.today() < timeToSetNextMeals: setNextDayMealTimes = sched.add_date_job(setTomorrowsMeals,timeToSetNextMeals)

lastTwitterStatusID = 1 #updateLastTweetID()

sched.add_interval_job(searchForTweets,minutes=1)