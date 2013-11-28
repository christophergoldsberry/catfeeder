import datetime

def setTime(hours, minutes):
	now = datetime.datetime.today()
	if now.hour > hours:
		return datetime.datetime(now.year, now.month, now.day+1, hours, minutes)
	else: return datetime.datetime(now.year, now.month, now.day, hours, minutes)

def feedingAction(meal, debug):
	if debug is True: print meal + " called."
	#ser.write('1')
	#api.PostUpdate(status="It's currently "+datetime.datetime.today().strftime("%c")+" and I should be getting fed my "+ meal + " meal. Meow!")