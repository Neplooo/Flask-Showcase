from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
from gpiozero import AngularServo

#RGB Ring stuff
import time
import random
from rpi_ws281x import PixelStrip, Color
import argparse
import keyboard

# LED strip configuration:
LED_COUNT = 16        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#Intialize the library (must be called once before other functions).
strip.begin()

app = Flask(__name__)

#Define Servo Pin
servoPin = 17

#Define Servo (GPIOZero)
servo = AngularServo(servoPin, min_angle=-180, max_angle=180)

#Set our GPIO mode
GPIO.setmode(GPIO.BCM)

#Default gateway (Main Menu)
@app.route("/")
def mainMenu():
    
    return render_template("mainMenu.html")

#Gateway for the open page
@app.route("/open")
def openServo():
    #Open the lock
    servo.angle = -90
    
    #Pull up the open.html page
    return render_template("open.html")

#Gateway for the close page
@app.route("/close")
def closeServo():
    #Close the lock
    servo.angle = 90
    
    #Pull up the close.html page
    return render_template("close.html")

@app.route("/slider", methods=['GET','POST'])
def pickAngle():
    
    if request.method == "POST":

         #Take the variable for range from the HTML
         servoRange = request.form["slider"]
    
         #close the lock
         servo.angle = int(servoRange)
    
         return render_template("slider.html")

    else:

         #Pull up the slider.html page
         return render_template("slider.html")
        
        
@app.route("/color", methods=["GET", "POST"])
def changeColor():
    
    if request.method == "POST":
        
        #Take the color value from the color picker
        colorVal = request.form["colorPicker"]
        
        #Print that value (Debug)
        #print(str(colorVal))
        
        #Convert our value from hex code to rgb value
        colorRGBVal= hex_to_rgb(colorVal)
        
        #Print the rgb value (Debug)
        #print(str(colorRGBVal))
        
        for x in range(16):
            strip.setPixelColor(x, Color(colorRGBVal[0], colorRGBVal[1], colorRGBVal[2]))
            strip.show()
            time.sleep(0.05)
        
        #Return our html page
        return render_template("colorPicker.html")
    
    else:
        
        #If nothing happens, return the html page
        return render_template("colorPicker.html")
    
#Some Guy's code that I stole that converts Hex to RGB
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#Run server on ip: 0.0.0.0
app.run(host="0.0.0.0")

GPIO.cleanup()

