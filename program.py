import RPi.GPIO as GPIO
from firebase import firebase
from time import sleep
import datetime
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.cleanup()
GPIO.setwarnings(False)



def setRelay(nyala):
    GPIO_RELAY = 18
    GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
    if nyala:
        GPIO.output(GPIO_RELAY, GPIO.LOW) # nyala
    else:
        GPIO.output(GPIO_RELAY, GPIO.HIGH) # mati
def setAutomasi():
    # matic mode
    suhu = firebase.get('sensor/dht','temp')
    if  suhu > 40:
        setRelay(True)
    else:
        setRelay(False)

def setManualisasi():
    if firebase.get('sensor/relay','status'):
        # relay on dari android
        setRelay(True)
        print("relay hidup")
    else:
        # relay off dari android
        setRelay(False)
        print("relay Mati")

        
while True:
    try:
        firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)
        while True:
            if firebase.get('sensor/relay','manual')==True:
               setManualisasi()
               sleep(1)
            else:
               setAutomasi()
               sleep(1)
          
        break
    except StandardError:
        setAutomasi()
        print "Not Connect Firebase. Please try again."

  

