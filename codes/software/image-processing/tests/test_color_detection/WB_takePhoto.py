#import RPi.GPIO as GPIO
import time
import os
import cv2
#----------

#GPIO.cleanup()

#GPIO.setmode(GPIO.BCM) 
#GPIO.setup(4, GPIO.OUT) 

#GPIO.output(4, GPIO.LOW)
#time.sleep(1)
#GPIO.output(4, GPIO.HIGH)

#Enable webcam
camera = cv2.VideoCapture(0)
return_value, image = camera.read()

# Take a photo and save it in the current folder 
cv2.imwrite('opencv'+'.png', image)

#GPIO.output(4,GPIO.LOW)
#GPIO.cleanup()
