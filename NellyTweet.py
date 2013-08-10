#This program sets up a feeding schedule for Nelly, and feeds her each day
#according to the schedule established.  Changes to the schedule (additions), 
#or evening meals (if we're out), or treats are handled by sending tweets to the
#nelly twitter account (@NellysFood)

#Import Libraries 
import twitter
from datetime import datetime
from threading import Timer
from apscheduler.scheduler import Scheduler #pip install APscheduler

#--------------------
#---Variables--------
#--------------------

#Set up a scheduler object


#Set Up API account access for @Nellysfood
consumer_key = 'DbAGiakC3vg040FJX8A7A'
consumer_secret= 'nAFnbwGi6gNb6MRUrqDamMxLSCW1A7OCF4FiepUQIWw'
access_token= '1646642456-zECt0bTkcUYQ3z5FFAjeYQbgmKLBGOX66PhiWsP'
access_token_secret= 'TxMQD7UO3miZTW4FNjcUJ77vHyVHXMraOL9n4Hx3MM'

#API is the twitter object that we will use to call twitter commands
api=twitter.Api(consumer_key= consumer_key,consumer_secret=consumer_secret,access_token_key=access_token,access_token_secret=access_token_secret)

#Set up initial meal schedules, roll feedings over to next day if time has already passed today
morningMeal = datetime.today().replace(hour=7,minute=30)
if (morningMeal - datetime.today()).total_seconds() < 0:
	morningMeal = morningMeal.replace(day=morningMeal.day+1)
eveningMeal = datetime.today().replace(hour=6,minute=30)
if (eveningMeal - datetime.today()).total_seconds() < 0:
	eveningMeal = eveningMeal.replace(day=eveningMeal.day+1)
midnightMeal = datetime.today().replace(hour=11,minute=30)
if (midnightMeal - datetime.today()).total_seconds() < 0:
	midnightMeal = midnightMeal.replace(day=midnightMeal.day+1)

# Each tweet has a unique id, which is constantly incrementing; this will get updated each time
# a tweet is read so we never duplicate an action requested by a tweet.
# it initalizes at one (THE BEGINNING OF TIIIIME)
lastTwitterID = 1

#only tweets from allowed users are parsed.  This is the user id array of allowed users.  Currently @goldsberry only.

allowedUsers= [14875882]

#-----------------------
#---Function Blocks
#-----------------------


# Determines whether the user is allowed to command Nelly's food bowl
def isAllowedUser(requestMaker):
	for user in allowedUsers:
		if user == requestMaker:
			return True
	return False


#Strips the first hashtag in the tweet and returns it as a command
def parseCommandWord(command):
	for word in command.split():
		if word.startswith("#"):
				requestedAction = word.strip("#")
				"""right now, this only returns the first hashtag in the tweet.  
				In the future, we could use .extend() to add more keywords to the list, and then use
				something like 'for COMMAND in REQUESTEDACTION:' etc etc. """
				return requestedAction

#updates either the morning, evening, or midnight feeding time.
def updateCorrectMealTimer(mealTimeToUpdate, newMealTime):
	if mealTimeToUpdate == morningMeal:
		morningMealTimer.cancel()
		morningMeal.replace(hour = newMealTime.hour, minute= newMealTime.minute)
		timeleft = morningMeal  - datetime.today()
		morningMealTimer = Timer(timeleft.total_seconds(), feedingAction)
		morningMealTimer.start()
	elif mealTimeToUpdate == eveningMeal:
		try:
			eveningMealTimer.cancel()
			eveningMeal.replace(hour = newMealTime.hour, minute= newMealTime.minute)
			if eveningMealScheduled is True: #it's not nessecarily the case that we have an active feeding scheduled for the evening.  if so, we reset the timer.
				timeleft = eveningMeal  - datetime.today()
				eveningMealTimer = Timer(timeleft.total_seconds(), feedingAction)
				eveningMealTimer.start()
		except NameError:
			print "no evening meal scheduled!"
	elif mealTimeToUpdate == midnightMeal:
		midnightMealTimer.cancel()
		midnightMeal.replace(hour = newMealTime.hour, minute= newMealTime.minute)
		timeleft = midnightMeal  - datetime.today()
		midnightMealTimer = Timer(timeleft.total_seconds(),feedingAction)
		midnightMealTimer.start()
	else:
		print mealTimeToUpdate + "is not updateable, because it not a meal keyword!"


#takes the twitter text, searches for a STRPtime-able word, and sets it as the new meal
def parseNewMealTimeFromTweet(text): 
	for word in text.split():
		#Try to strip each word, in series into a datetime.  Tweets will be written in #:##AM/PM format.
		try:
			newMealTime = datetime.strptime(word,"%I:%M%p")
			return newMealTime
		except ValueError:
			print "not a strippable object, moving on to next"

#takes the twitter text, searches for a STRPtime-able word, and sets it as the new meal
def getCorrectMealFromTweet(text): 
	for word in text.split():
		#Try to strip each word, in series into a datetime.  Tweets will be written in #:##AM/PM format.
		if word.lower() == 'morning':
			return morningMeal
		elif word.lower() = 'evening':
			return eveningMeal
		elif word.lower() = 'midnight':
			return midnightMeal
		else:
			print "no meal specified, changing morning meal by default"
			return morningMeal


#Searches for tweets, and executes a command
def searchForTweets():
	#print str(datetime.now().hour) + ":" + str(datetime.now().minute)
	mention = api.GetMentions(since_id=str(lastTwitterID)) #calls for mentions greater than last recorded mention
	#mention.id if statement will fail silently if no new mentions exist
	if mention[0].id > lastTwitterID && isAllowedUser(mention[0].user.id):
		lastTwitterID = mention[0].id
		user = mention[0].user.id
		command = parseCommand(mention[0].text)
		fullText = mention[0].text
		statusID = mention[0].id
		#determine what kind of command has been made
		if command in controlOptions:
			controlOptions[command](fullText)
		else:
			api.PostUpdate(status="I don't recognize that command! I'm just going to go back to sleep. I mean, uh, meow.",in_reply_to_status_id=statusID)

	#if (mention[0].text).find('test'):
	#if (mention[0].user.name) == 'goldsberry':
		#print "this came from golds"
	#print str(datetime.now().hour) + ":" + str(datetime.now().minute)

def updateMealTime(text):
	mealTimeToUpdate = getCorrectMealFromTweet(text)
	newMealTime = parseNewMealTimeFromTweet(text)
	updateCorrectMealTimer(mealTimeToUpdate,newMealTime)

def setNextMeals():
	nextMorningMeal = morningMeal.replace(day=morningMeal.day+1)
	nextEveningMeal = eveningMeal.replace(day=eveningMeal.day+1)
	nextMidnightMeal = midnightMeal.replace(day=midnightMeal.day+1)

def feedingAction():
	api.PostUpdate(status="It's currently "+datetime.today().strftime("%c")+" and I should be getting fed! Meow!")
#Function Dictionary
controlOptions = {'updateMealTime' : updateMealTime
				  'addEveningMeal' : addEveningMeal
				  'giveTreat' : giveTreat
}

tweetSearch= Timer(60,searchForTweets)
tweetSearch.start()

setNextMeals()

morningMealTimer = Timer((morning)

