from goprocam import GoProCamera
from goprocam import constants
import time

# Connect GoPro
gpCam = GoProCamera.GoPro()

# Take a photo and save it in the current folder 
gpCam.downloadLastMedia(gpCam.take_photo(0)) 



