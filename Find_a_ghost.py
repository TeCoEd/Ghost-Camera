#!/usr/bin/env python
#ghost evidence, 1)movement, 2)change in temp, 3)colour / light 
import sys
import os
import time
import picamera
import RPi.GPIO as GPIO
from envirophat import light, weather, motion, leds, analog

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)

#variables for the motion sensing#
threshold = 0.2
readings = []
last_z = 0

global file_name
file_name = "0"
analog_values = analog.read_all()
print (analog_values)

#set up a function for the camera#
def catch_a_ghost():
    global file_name
    with picamera.PiCamera() as camera:
            GPIO.output(10, GPIO.HIGH)
            time.sleep(0.2)
            #camera.start_preview() #remove
            #time.sleep(2) #remove
            print (file_name)
            camera.capture(file_name + ".jpg")
            time.sleep(0.3)
            GPIO.output(10, GPIO.LOW)
            file_name = int(file_name) + int(1)
            file_name = str(file_name)
            os.system('mpg321 /home/pi/wegotone.mp3 @')
            

###establish the temperature of the room###
start_temp = weather.temperature()
print ("The room is ", start_temp)

try:
    while True:
        current_temp = weather.temperature()
        print ("Current Temerature is", current_temp)
        #time.sleep(8)

        #Sense any movement#
        readings.append(motion.accelerometer().z)
        readings = readings[-4:]
        z = sum(readings) / len(readings)
        time.sleep(0.3)

        #read the amount of light#
        amount_of_light = light.light()
        r, g, b = light.rgb()
    
        print("Amount of light", amount_of_light)
        print ("Colour", r, g, b)
    
        time.sleep(1)

        """Check for motion or movement"""
        if last_z > 0 and abs(z-last_z) > threshold:
            print("Motion Detected!!!")
            catch_a_ghost()
            leds.on()
        last_z = z
        time.sleep(0.01)
        leds.off()

        """Check for a change in temperature""" 
        if current_temp - start_temp > 5:
            print ("GHOST")
            catch_a_ghost()
            start_temp = current_temp

        if amount_of_light > 2:
            print ("GHOST")
            catch_a_ghost()

except KeyboardInterrupt:
    pass
