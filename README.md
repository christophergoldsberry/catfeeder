<<<<<<< HEAD
# Twitter, Raspberry Pi and Arduino-Powered Cat Feeder

### It's complicated, but it's the only way I know how to do it (right now)

---

#####Concept:

1. A Raspberry Pi has a set of feedings scheduled to repeat daily

2. When those feeding actions are called, the RPi sends a serial comamnd to an Arduino

3. The serial command is read by the Arduino, which turns a stepper motor, driving a food hopper.

4. Througout the day, the RPi scans twitter for activity on the account @nellysfood.

5. If certain hashtags are found in @ mentions, the RPi directs the Arduino to perform different actions

---

#####Current Contents:

1. NellyTweet.py: This is the python script to be run by the Raspberry Pi.

***TO BE ADDED***

2. MotorControl.ino: this is the sketch executed by the Arduino which listens to serial communication.

3. Wiring Diagram: The RPi connects to Arduino via USB B->A Cable. The Arduino has an Adafruit motor shield, which drives the Stepper.

---

####Dependencies:

***NellyTweet.py***
Libraries Used: 
twitter
datetime
Scheduler (from APScheduler)
Choice (from Random)
Logging

***MotorControl.ino***
Adafruit Motor Shield Library (#AFmotor)
