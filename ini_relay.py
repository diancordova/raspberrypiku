import RPi.GPIO as GPIO
from firebase import firebase
from time import sleep
import datetime
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.cleanup()
GPIO.setwarnings(False)

firebase = firebase.FirebaseApplication(
    'https://smart-greenhouse-92747.firebaseio.com/', None)


def update_relay():
    result = firebase.get('/sensor/relay', 'status')
    result1 = firebase.get('/sensor/dht','temp')
    print result1
    if result==True:
        GPIO_RELAY = 18
        GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
        GPIO.output(GPIO_RELAY, GPIO.LOW)  # out
        GPIO.output(GPIO_RELAY, GPIO.LOW)
	print('Relay Nyala')
    # print('result1')
    if result==False:
        GPIO_RELAY = 18
        GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
        GPIO.output(GPIO_RELAY, GPIO.HIGH)  # out
        GPIO.output(GPIO_RELAY, GPIO.HIGH)
	print('Relay Mati')
    if result1<30:
        GPIO_RELAY = 18
        GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
        GPIO.output(GPIO_RELAY, GPIO.HIGH)  # out
        GPIO.output(GPIO_RELAY, GPIO.HIGH)
        firebase.patch('/sensor/relay', {"status":False})
	print('Suhu Normal')
    if result1>29:
        print('Suhu Panas kipas blower menyala!!')
        GPIO_RELAY = 18
        GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
        GPIO.output(GPIO_RELAY, GPIO.LOW)  # out
        GPIO.output(GPIO_RELAY, GPIO.LOW)
        firebase.patch('/sensor/relay', {"status":True})



while True:
    update_relay()
