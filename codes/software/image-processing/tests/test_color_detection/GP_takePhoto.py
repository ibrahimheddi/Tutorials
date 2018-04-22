from goprocam import GoProCamera
from goprocam import constants
#import RPi.GPIO as GPIO
import time
import os
#----------

#GPIO.cleanup()

#GPIO.setmode(GPIO.BCM) 
#GPIO.setup(4, GPIO.OUT) 

# Connect GoPro
gpCam = GoProCamera.GoPro()

#GPIO.output(4, GPIO.LOW)
#time.sleep(1)
#GPIO.output(4, GPIO.HIGH)

# Take a photo and save it in the current folder 
gpCam.take_photo(0)
gpCam.downloadLastMedia()
image = gpCam.getMediaInfo('file')

os.rename("100GOPRO-"+ image[0:9]+"JPG","opencv.png")


#GPIO.output(4,GPIO.LOW)
#GPIO.cleanup()
