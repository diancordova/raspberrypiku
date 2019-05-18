import RPi.GPIO as GPIO
from firebase import firebase
from time import sleep
import datetime
import os
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.cleanup()
GPIO.setwarnings(False)

firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)
        

def setRelayPompaA(nyala):
  PIN_POMPAA = 24
  GPIO.setup(PIN_POMPAA, GPIO.OUT)  # GPIO Assign mode
  if nyala:
      firebase.patch('/sensor/relay1', {"isLoading":False}) 
      GPIO.output(PIN_POMPAA, GPIO.LOW) # nyala
      print("Pompa A Nyala")
  else:
      firebase.patch('/sensor/relay1', {"isLoading":False}) 
      GPIO.output(PIN_POMPAA, GPIO.HIGH) # mati
      print("Pompa A Mati")
 
     
def setRelayPompaB(nyala):
  PIN_POMPAB = 25
  GPIO.setup(PIN_POMPAB, GPIO.OUT)  # GPIO Assign mode
  if nyala:
      firebase.patch('/sensor/relay1', {"isLoading":False}) 
      GPIO.output(PIN_POMPAB, GPIO.LOW) # nyala
      print("Pompa B Nyala")
  else:
      firebase.patch('/sensor/relay1', {"isLoading":False}) 
      GPIO.output(PIN_POMPAB, GPIO.HIGH) # mati
      print("Pompa B Mati")
      
  

while True:
        statusPompaA = firebase.get('sensor/relay1','status')
        statusPompaB = firebase.get('sensor/relay2','status')
        if statusPompaA:
            setRelayPompaA(statusPompaA)
        else:
            setRelayPompaA(statusPompaA)
        if statusPompaB:
            setRelayPompaB(statusPompaB)
        else: 
            setRelayPompaB(statusPompaB)
        sleep(0)