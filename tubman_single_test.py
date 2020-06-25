
from datetime import datetime
import csv
import os
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

## Fan relay pin 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)

##Humidifier relay pin 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
GPIO.output(12,GPIO.HIGH)


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN_TUB1 = 4
DHT_PIN_TUB2 = 5



##Tub 1 Sensor reading
while True:
    humid_time=0
    humidity_tub1, temperature_tub1 = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN_TUB1)
    if humidity_tub1 is not None and temperature_tub1 is not None:
        tempf_tub1 = temperature_tub1 *1.8 + 32
        temp1 = round(tempf_tub1,1)
                   
## Tub2 sensor reading        
    humidity_tub2, temperature_tub2 = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN_TUB2)
    if humidity_tub2 is not None and temperature_tub2 is not None:
        tempf_tub2 = temperature_tub2 *1.8 + 32
        temp2 = round(tempf_tub2,1)
                              
##Humidity control tub1
              
        if(humidity_tub2 < 97):
            humid_time=10
            GPIO.output(12,GPIO.LOW)
            print("Tub 2 Humid on")
            time.sleep(30)  
                ##Fan1 on
            GPIO.output(18,GPIO.LOW)
            time.sleep(4)
                ##Fan1 off
            GPIO.output(18,GPIO.HIGH)
                ##fogger off
            GPIO.output(12,GPIO.HIGH)
        if(humidity_tub2>97):
           GPIO.output(12,GPIO.HIGH)

    
    
    ##logging tub2    
        f=open("Tub2_log.csv", "a", newline="")
        wc=csv.writer(f)

        wc.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tempf_tub2, humidity_tub2, tempf_tub1, humidity_tub1, humid_time])
        f.close()
        humid_time=0
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    

    # Write four lines of text.

    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+8),     "T1= " + str(temp1) + " Hmd1=" + str(humidity_tub1), font=font, fill=255)
    draw.text((x, top+16),    "T2= " + str(temp2) + " Hmd2=" + str(humidity_tub2), font=font, fill=255)
    

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)

else:
    print("Sensor failure. Check wiring.");
    time.sleep(2);
  




