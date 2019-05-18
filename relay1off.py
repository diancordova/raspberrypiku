import RPi.GPIO as GPIO
from firebase import firebase
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

RELAIS_1_GPIO = 18
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # out
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)


firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)

def update_firebase():
    firebase.patch('/sensor/relay', {"status":False})


while True:
		update_firebase()

