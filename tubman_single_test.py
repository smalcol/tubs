
from datetime import datetime
import csv
import os
import Adafruit_DHT
import time
import RPi.GPIO as GPIO

## Heater relay pin 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)

##Humidifier relay pin 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
GPIO.output(12,GPIO.HIGH)

##Fan1 relay pin 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
GPIO.output(5,GPIO.LOW)
 
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN_TUB1 = 4
DHT_PIN_TUB2 = 5



##Tub 1 Sensor reading
while True:
    humidity_tub1, temperature_tub1 = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN_TUB1)
    if humidity_tub1 is not None and temperature_tub1 is not None:
        tempf_tub1 = temperature_tub1 *1.8 + 32
        print("Temp_tub1_test={0:0.1f}F Humidity_tub1={1:0.1f}%".format(tempf_tub1, humidity_tub1))
        
    
## Tub2 sensor reading        
    humidity_tub2, temperature_tub2 = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN_TUB2)
    if humidity_tub2 is not None and temperature_tub2 is not None:
        tempf_tub2 = temperature_tub2 *1.8 + 32
        print("Temp_tub2={0:0.1f}F Humidity_tub2={1:0.1f}%".format(tempf_tub2, humidity_tub2))
 
           

           
##Humidity control tub1
              
        if(humidity_tub2 < 95):
            GPIO.output(12,GPIO.LOW)
            print("Tub 2 Humid on")
            time.sleep(20)  
                ##Fan1 on
            GPIO.output(18,GPIO.LOW)
            time.sleep(2)
                ##Fan1 off
            GPIO.output(18,GPIO.HIGH)
                ##fogger off
            GPIO.output(12,GPIO.HIGH)
        if(humidity_tub2>96):
            print ("Tub 2 humid off")
            GPIO.output(12,GPIO.HIGH)

    ##Fan control (overheating tub1)
        if(tempf_tub1>90):
            print ("Tub 1 Fan on")
            GPIO.output(5,GPIO.LOW)
            time.sleep(2)
            print ("Tub 1 Fan off")
            GPIO.output(5,GPIO.HIGH)
    
    ##logging tub2    
        f=open("Tub2_log.csv", "a", newline="")
        wc=csv.writer(f)

        wc.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tempf_tub2, humidity_tub2])
        f.close()

else:
    print("Sensor failure. Check wiring.");
    time.sleep(2);
  




