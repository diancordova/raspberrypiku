import RPi.GPIO as GPIO
from firebase import firebase
import time
import os
import datetime
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.cleanup()
GPIO.setwarnings(False)



firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)

def baca_automasi():
    automasi = firebase.get('/sensor/relay', 'manual')
    if automasi==False:
      os.system ("sudo /usr/bin/python iti_relay1.py")
      print('Manualisasi Berjalan')
      print automasi
      time.sleep(1)
    if automasi==True:
      os.system ("sudo /usr/bin/python ini_relay1.py")
      print automasi
      print('Automasi Berjalan ')
      time.sleep(1)
print 'error'

while True:
    baca_automasi()
