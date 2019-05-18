from time import sleep
import datetime
from firebase import firebase
import serial
import json
import sys
import re
import RPi.GPIO as GPIO
import Adafruit_DHT
import urllib2, urllib, httplib
from functools import partial

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

# Sensor Suhu DHT11 #
sensor = Adafruit_DHT.DHT11
pin = 17
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


# Koneksi ke Firebase alamat firebase
firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)

# Pembacaan Data sensor dari ADC Arduino melalu SerialUSB #
device = '/dev/ttyUSB0' 


print "Trying...",device
arduino = serial.Serial(device, 9600)
print "connected to arduino ",device
def update_firebase():
   data1 = arduino.readline()  
   print "Sensor Nutrisi TDS:", data1
   sleep(0)
   data2 = arduino.readline()  
   print "Sensor PH", data2
   sleep(0)
   data3 = arduino.readline()  
   print "Sensor Cahaya PhotoDioda:", data3
   sleep(0)
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   print "Suhu :", temperature
   sleep(0)
   print "Kelembapan:", humidity
   sleep(3)

   # regex data dari readline
   nilaiTds= re.findall(r',?([^,]+)(?:,|\r\n)', data1)
   nilaiPH= re.findall(r',?([^,]+)(?:,|\r\n)', data2)
   nilaiCahaya=re.findall(r',?([^,]+)(?:,|\r\n)', data3)

   # convert ke int dan float
   nilai1 =float(nilaiTds[0])
   nilai2 =float(nilaiPH[0])
   nilai3 =float(nilaiCahaya[0])

  

  
   data = {"tds/value": nilai1, "ph/value": nilai2,"photoDioda/value/" :nilai3,"dht/humidity": humidity,"dht/temp":temperature}
   firebase.patch('/sensor/', data)   
while True:
   update_firebase()
   sleep(1)







