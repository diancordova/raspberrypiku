import RPi.GPIO as GPIO
from firebase import firebase


GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 18
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
GPIO.output(RELAIS_1_GPIO, GPIO.LOW)




firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)
firebase.patch('/sensor/relay', {"status":True})

