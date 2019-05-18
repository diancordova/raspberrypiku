import RPi.GPIO as GPIO
from firebase import firebase
from time import sleep
import datetime
import Adafruit_DHT

import urllib2, urllib, httplib
import json
from functools import partial
GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
GPIO.cleanup()
GPIO.setwarnings(False)



  
# ===== Definisi Pin GPIO====== #
GPIO_RELAY = 18
GPIO_RELAY1 = 27 
PIN_SPRINGKLER = 24
PIN_AIR = 25
pin = 17

# SUHU DHT #
#-----------------------------------********************---------------------------------------------#
#-----------------------------MULAI MENGERJAKAN METODE FUZZY-----------------------------------------#
####---------------------------------*******************-----------------------------------------#####
# firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)


# Function set suhu

def setRelay(nyala):
  firebase.patch('/sensor/relay', {"isLoading":False})
  GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
  if nyala:
      GPIO.output(GPIO_RELAY, GPIO.LOW) # nyala
      print("relay hidup")
      firebase.patch('/sensor/relay', {"status":True})
  else:
      GPIO.output(GPIO_RELAY, GPIO.HIGH) # mati
      
     
def setRelaySpringkler(nyala):
  firebase.patch('/control/relaySpringkler', {"manual":True})
  GPIO.setup(PIN_SPRINGKLER, GPIO.OUT)  # GPIO Assign mode
  if nyala:
      GPIO.output(PIN_SPRINGKLER, GPIO.LOW) # nyala
      print("Springkler Hidup")
  else:
      GPIO.output(PIN_SPRINGKLER, GPIO.HIGH) # mati
      print("Springkler Mati")

def setRelayAir(nyala):
  firebase.patch('/sensor/relay2', {"manual":True})
  GPIO.setup(PIN_AIR, GPIO.OUT)  # GPIO Assign mode
  if nyala:
      GPIO.output(PIN_AIR, GPIO.LOW) # nyala
      print("air hidup")
     
  else:
      GPIO.output(PIN_AIR, GPIO.HIGH) # mati
      print("air mati")


def setManualisasi():
  if firebase.get('sensor/relay','status'):
    # relay on dari android
    setRelay(True)
  else:
    # relay off dari android
    if firebase.get('sensor/relay','manual'):
       setRelay(True)
    else:
       setRelay(False)
       print("relay mati")

def setSpringklerNyala():
    if firebase.get('control/relaySpringkler','status'):
       setRelaySpringkler(True)
    else:
       setRelaySpringkler(False)

def setAirNyala():
    if firebase.get('sensor/relay2','status'):
       setRelayAir(True)
    else:
       setRelayAir(False)
       
def setPompaNutrisiNyala():
    print "pompa nutrisi dan air nyala"
    firebase.patch('/sensor/relay', {"status":True})
    GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
    GPIO.output(GPIO_RELAY, GPIO.LOW) # nyala


    
def setPompaAirNyala():
    print "pompa nyala"
    firebase.patch('/sensor/relay', {"status":True})
    GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
    GPIO.setup(GPIO_RELAY1, GPIO.OUT)  # GPIO Assign mode    
    GPIO.output(GPIO_RELAY, GPIO.LOW) # nyala
    GPIO.output(GPIO_RELAY1, GPIO.LOW) # nyala
def setPompaMati():
    print "pompa mati"
    firebase.patch('/sensor/relay', {"status":False})
    GPIO_RELAY = 18
    GPIO_RELAY1 = 19 
    GPIO.setup(GPIO_RELAY, GPIO.OUT)  # GPIO Assign mode
    GPIO.setup(GPIO_RELAY1, GPIO.OUT)  # GPIO Assign mode    
    GPIO.output(GPIO_RELAY, GPIO.HIGH) # nyala
    GPIO.output(GPIO_RELAY1, GPIO.HIGH) # nyala

def setAutomasiMetode():
    sensorPH = float (firebase.get('/sensor/ph', 'value'))
    sensorSuhu = float (firebase.get('/sensor/suhu', 'temp'))
    sensorNutrisi = float (firebase.get('/sensor/tds','value'))
    nutrisi1Tumbuhan = float (firebase.get('/pilihTumbuhan','firstValue'))
    nutrisi2Tumbuhan = float (firebase.get('/pilihTumbuhan','secondValue'))
    medianNutrisi = float ((nutrisi1Tumbuhan+nutrisi2Tumbuhan)/2)

    # print ('ph:',sensorPH)
    # print ('suhu:',sensorSuhu)
    # print ('nutrisi',sensorNutrisi)
    # print ('nutrisi1',nutrisi1Tumbuhan)
    # print ('nutrisi2',nutrisi2Tumbuhan)
    # print ('median',medianNutrisi)

    nilaiZnormal = 0
    nilaiZkurangAir = 1
    nilaiZkurangNutrisi = 2
   
  ###__________FUZZIFIKASI_________###
  ####_____________________________####
  ##**********SENSOR PH************##  
    #PH_ASAM
    if sensorPH <= 6.5:
      sensorPH_asam = 1
    if sensorPH >= 6 and sensorPH <= 6.5:
      sensorPH_asam = float (6.5 - sensorPH) / (6.5-6)
    if sensorPH >=6.5:
      sensorPH_asam = 0
      
    #PH_NETRAL

    if sensorPH <= 6.5 or sensorPH >=8.5:
      sensorPH_netral = 0
    if sensorPH >= 6 and sensorPH <= 7:
      sensorPH_netral = float (sensorPH - 6) / (7-6)
    if sensorPH >= 7 and sensorPH <= 8.5:
      sensorPH_netral = float (8.5- sensorPH) / (8.5-7)

    #PH_BASA

    if sensorPH <= 7:
      sensorPH_basa = 0
    if sensorPH >= 7 and sensorPH <= 8.5:
      sensorPH_basa =float (sensorPH-7) / (8.5-7)
    if sensorPH >=8.5:
      sensorPH_basa =1

  ##**********SENSOR SUHU************##  
      #SUHU_DINGIN

    if sensorSuhu <= 23:
      sensorSuhu_dingin = 1
    if sensorSuhu >= 23 and sensorSuhu <= 26:
      sensorSuhu_dingin = float (26 - sensorSuhu) / (26-23)
    if sensorSuhu >=26:
      sensorSuhu_dingin = 0
      
    #SUHU_NORMAL

    if sensorSuhu <= 23 or sensorSuhu >=30:
      sensorSuhu_normal = 0
    if sensorSuhu >= 23 and sensorSuhu <= 26:
      sensorSuhu_normal = float (sensorSuhu - 23) / (26-23)
    if sensorSuhu >= 26 and sensorSuhu <= 30:
      sensorSuhu_normal = float (30- sensorSuhu) / (30-26)

    #SUHU_PANAS

    if sensorSuhu <= 26:
      sensorSuhu_panas = 0
    if sensorSuhu >= 26 and sensorSuhu <= 30:
      sensorSuhu_panas = float (sensorSuhu-26) / (30-26)
    if sensorSuhu >=30:
      sensorSuhu_panas =1
  ##**********SENSOR NUTRISI************##  
    #NUTRISI_KURANG

    if sensorNutrisi <= nutrisi1Tumbuhan:
      sensorNutrisi_kurang = 1
    if sensorNutrisi >= nutrisi1Tumbuhan and sensorNutrisi <= medianNutrisi:
      sensorNutrisi_kurang = float (medianNutrisi - sensorNutrisi) / (medianNutrisi-nutrisi1Tumbuhan)
    if sensorNutrisi >=medianNutrisi:
      sensorNutrisi_kurang = 0
      
    #NUTRISI_NORMAL

    if sensorNutrisi <= nutrisi1Tumbuhan or sensorNutrisi >=nutrisi2Tumbuhan:
      sensorNutrisi_normal = 0
    if sensorNutrisi >= nutrisi1Tumbuhan and sensorNutrisi <= medianNutrisi:
      sensorNutrisi_normal = float (sensorNutrisi-nutrisi1Tumbuhan)/(medianNutrisi-nutrisi1Tumbuhan)
    if sensorNutrisi >= medianNutrisi and sensorNutrisi <= nutrisi2Tumbuhan:
      sensorNutrisi_normal = float (nutrisi2Tumbuhan-sensorNutrisi) / (nutrisi2Tumbuhan-medianNutrisi)

    
       
    #NUTRISI_LEBIH
    if sensorNutrisi <= medianNutrisi:
      sensorNutrisi_lebih = 0
    if sensorNutrisi >= medianNutrisi and sensorNutrisi <= nutrisi2Tumbuhan:
       sensorNutrisi_lebih = float (sensorNutrisi-medianNutrisi)/(nutrisi2Tumbuhan-medianNutrisi)
    if sensorNutrisi >=nutrisi2Tumbuhan:
      sensorNutrisi_lebih =1

    alpha_predikat1tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_asam,1),sensorSuhu_dingin)
    alpha_predikat2tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_asam,1),sensorSuhu_normal)
    alpha_predikat3tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_asam,1),sensorSuhu_panas)
    alpha_predikat4tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_netral,1),sensorSuhu_dingin)
    alpha_predikat5tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_netral,1),sensorSuhu_normal)
    alpha_predikat6tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_netral,1),sensorSuhu_panas)
    alpha_predikat7tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_basa,1),sensorSuhu_dingin)
    alpha_predikat8tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_basa,1),sensorSuhu_normal)
    alpha_predikat9tambahnutrisidanair = min(sensorNutrisi_kurang,round(sensorPH_basa,1),sensorSuhu_panas)
    alpha_predikat10tambahair=min(sensorNutrisi_normal,round(sensorPH_asam,1),sensorSuhu_dingin)
    alpha_predikat11tambahair=min(sensorNutrisi_normal,round(sensorPH_asam,1),sensorNutrisi_normal)
    alpha_predikat12tambahair=min(sensorNutrisi_normal,round(sensorPH_asam,1),sensorSuhu_panas)
    alpha_predikat13tambahair=min(sensorNutrisi_normal,round(sensorPH_netral,1),sensorSuhu_dingin)
    alpha_predikat14normal=min(sensorNutrisi_normal,round(sensorPH_netral,1),sensorSuhu_normal)
    alpha_predikat15tambahair=min(sensorNutrisi_normal,round(sensorPH_netral,1),sensorSuhu_panas)
    alpha_predikat16tambahair=min(sensorNutrisi_normal,round(sensorPH_basa,1),sensorSuhu_dingin)
    alpha_predikat17tambahair=min(sensorNutrisi_normal,round(sensorPH_basa,1),sensorSuhu_normal)
    alpha_predikat18tambahair=min(sensorNutrisi_lebih,round(sensorPH_basa,1),sensorSuhu_panas)
    alpha_predikat19tambahair=min(sensorNutrisi_lebih,round(sensorPH_asam,1),sensorSuhu_dingin)
    alpha_predikat20tambahair=min(sensorNutrisi_lebih,round(sensorPH_asam,1),sensorSuhu_normal)
    alpha_predikat21tambahair=min(sensorNutrisi_lebih,round(sensorPH_asam,1),sensorSuhu_panas)
    alpha_predikat22tambahair=min(sensorNutrisi_lebih,round(sensorPH_netral,1),sensorSuhu_dingin)
    alpha_predikat23tambahair=min(sensorNutrisi_lebih,round(sensorPH_netral,1),sensorSuhu_normal)
    alpha_predikat24tambahair=min(sensorNutrisi_lebih,round(sensorPH_netral,1),sensorSuhu_panas)
    alpha_predikat25tambahair=min(sensorNutrisi_lebih,round(sensorPH_basa,1),sensorSuhu_dingin)
    alpha_predikat26tambahair=min(sensorNutrisi_lebih,round(sensorPH_basa,1),sensorSuhu_normal)
    alpha_predikat27tambahair=min(sensorNutrisi_lebih,round(sensorPH_basa,1),sensorSuhu_panas)

    ## MENCARI NILAI MAX dari tiap konsekuensi fungsi implikasi ##

    maxNormal = alpha_predikat14normal
    maxTambahAir = max(alpha_predikat10tambahair,alpha_predikat11tambahair,alpha_predikat12tambahair,alpha_predikat13tambahair,alpha_predikat15tambahair,alpha_predikat16tambahair,alpha_predikat17tambahair,alpha_predikat18tambahair,alpha_predikat19tambahair,alpha_predikat20tambahair,alpha_predikat21tambahair,alpha_predikat22tambahair,alpha_predikat23tambahair,alpha_predikat24tambahair,alpha_predikat25tambahair,alpha_predikat26tambahair,alpha_predikat27tambahair)
    maxTambahNutrisiDanAir = max(alpha_predikat1tambahnutrisidanair,alpha_predikat2tambahnutrisidanair,alpha_predikat3tambahnutrisidanair,alpha_predikat4tambahnutrisidanair,alpha_predikat5tambahnutrisidanair,alpha_predikat6tambahnutrisidanair,alpha_predikat7tambahnutrisidanair,alpha_predikat8tambahnutrisidanair,alpha_predikat9tambahnutrisidanair)

    predikatXkonsekuen=(maxNormal*nilaiZnormal)+(maxTambahAir*nilaiZkurangAir)+(maxTambahNutrisiDanAir*nilaiZkurangNutrisi)
    hasilJumlahPredikat= maxNormal+maxTambahAir+maxTambahNutrisiDanAir
    bobotRatarata = predikatXkonsekuen/hasilJumlahPredikat
   


    

    if bobotRatarata <= 0.75 :
      status = "Normal"
      pompaAir = "Mati"
      pompaNutrisi = "Mati"
      setPompaMati()
    if bobotRatarata > 0.75 and bobotRatarata <= 1.5 :
      status = "Kurang Air"
      pompaAir = "Menyala"
      pompaNutrisi = "Mati"
      setPompaAirNyala()
    if bobotRatarata > 1.5 :
      status = "Kurang Nutrisi"
      pompaAir = "Menyala"
      pompaNutrisi = "Menyala"
      setPompaNutrisiNyala()
      # os.system ("sudo /usr/bin/python ini_relay1.py")
    print ('status',status)
    print ('pompaAir',pompaAir)
    print ('pompaNutrisi',pompaNutrisi)
    print ('ph:',sensorPH)
    print ('suhu:',sensorSuhu)
    print ('nutrisi',sensorNutrisi)
    print ('nutrisi1',nutrisi1Tumbuhan)
    print ('nutrisi2',nutrisi2Tumbuhan)
    print ("INI JUMLAH BOBOT ANDA :",bobotRatarata)
    print ('status',status)
    print ('pompaAir',pompaAir)
    print ('pompaNutrisi',pompaNutrisi)
    firebase.patch('/sensor/relay', {"isLoading1":False})
     

while True:
    try:
        firebase = firebase.FirebaseApplication('https://smart-greenhouse-92747.firebaseio.com/', None)
        while True:
            setSpringklerNyala()
            setAirNyala()
            if firebase.get('sensor/relay','manual')==True:
               setManualisasi()
               sleep(1)
            else:
               setAutomasiMetode()
               sleep(1)
        break
    except StandardError:
        setAutomasiMetode()
        print "Not Connect Firebase. Please try again."