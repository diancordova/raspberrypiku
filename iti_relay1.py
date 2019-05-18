import RPi.GPIO as GPIO
from firebase import firebase
from time import sleep
import datetime
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.cleanup()
GPIO.setwarnings(False)

GPIO_RELAY = 18
GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
GPIO.output(GPIO_RELAY, GPIO.HIGH)  # out
GPIO.output(GPIO_RELAY, GPIO.HIGH)

