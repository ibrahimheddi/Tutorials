#!/usr/bin/expect

#switch to "go pro wifi"

nmcli c up "armen" 
sleep 10
python3 GP_takePhoto.py


#switch to "robot wifi"

nmcli c up "Airport Express Lenaerts" 


python2 color_detection.py
