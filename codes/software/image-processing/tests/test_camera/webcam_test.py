import time
import cv2

# Create an object called camera and connect the firt camera to the computer
camera = cv2.VideoCapture(0)


# Take a photo and save it in the current folder 
return_value, image = camera.read()
cv2.imwrite('opencv'+'.png', image)



