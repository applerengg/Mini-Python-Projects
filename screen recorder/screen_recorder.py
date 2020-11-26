import cv2
import numpy as np 
import pyautogui
from datetime import datetime
import os

def getTimestampString():
    return "_".join(str(datetime.now()).split(" ")).replace(":", ".")[:-7]

version = "0.0.1"	# 2020.01.06
print("""
### Simple Screen Recorder ###
###       by appleren      ###
###         v {}        ###
""".format(version))

if not os.path.exists('video_captures'):
    os.makedirs('video_captures')

codec = cv2.VideoWriter_fourcc(*"XVID")
resolution = (1920, 1080)
FPS = 15#float(input("FPS: "))

date = getTimestampString()
save_location = "video_captures/vid_{}.avi".format(date)

output = cv2.VideoWriter(save_location, codec, FPS, resolution)
print("PRESS <ESC> ON THE PREVIEW WINDOW TO CLOSE AND SAVE VIDEO CAPTURE")

while True:
	ss = pyautogui.screenshot()			# get screenshot
	ss_array = np.array(ss)				# frame
	ss_array = cv2.cvtColor(ss_array, cv2.COLOR_BGR2RGB)	# fix frame colors for cv2

	output.write(ss_array)				# add ss frame to output file
	
	cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
	cv2.resizeWindow("screen", (resolution[0]*2//10, resolution[1]*2//10))
	cv2.imshow("screen", ss_array)		# show screen

	if cv2.waitKey(1) == 27:			# ESC is pressed
		break

print("Successfully saved on location: {}".format(save_location))
output.release()