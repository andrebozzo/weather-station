from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 15
camera.contrast = 50
camera.brightness = 50
camera.start_preview()
sleep(5)
'''
for awb in camera.AWB_MODES:
	camera.awb_mode = awb
	camera.annotate_text = "awb mode: %s" % awb
	sleep(5)
	camera.capture("/home/pi/Desktop/AWBphoto%s.jpg" % awb)
'''
camera.capture("/home/pi/Desktop/snapshot.jpg")
camera.stop_preview()
