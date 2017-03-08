import cv2
import numpy as np
import math
import serial
import threading
from time import sleep
from time import time

import random

DEBUG_MODE = 1

n = True
per = 50000
countper = 0
thingabob = per
class MockSerial:
	def readline(self):
		global thingabob, per, countper, n
		if countper >= 8:
			countper = 0
			n = bool(random.getrandbits(1))
			print("Type: " + str(n))
			return ("shooter\n" if n else "gears\n").encode()
		if thingabob:
			thingabob -= 1
			return "".encode()
		else:
			thingabob = per
			countper += 1
			return ("shooter\n" if n else "gears\n").encode()
		#return "waffles\n".encode()
		
	def write(self, data):
		pass
		print( data.decode(), end="")


if DEBUG_MODE:
	ser = MockSerial()
else:
	ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)	#on the pi it's AMA0

class FuncThread(threading.Thread):
	def __init__(self, target, *args):
		threading.Thread.__init__(self)
		self._target = target
		self._args = args
	def run(self):
		self._target(*self._args)

SCREEN_X = 640
SCREEN_Y = 480
SMALL_VAL = 0.1	#magic number 1
FOV_X = 61		#pulled from online? Mostly a guess
FOV_Y = 34
REF_THETA = 45	#SPECIFY		#angle the camera is mounted
REF_TOW_H = 2.35
REF_CAM_H = 0.8#.8.85 #SPECIFY		#height of camera on the robot above the ground
DILATE_ITERATIONS = 0
ERODE_ITERATIONS = 0

cap = cv2.VideoCapture(0)

frame = None

lower_g = np.array([65, 100, 100])
upper_g = np.array([85, 255, 255])

data = ["", "", "", ""]

def scrn21x(x):
	return (x / SCREEN_X)*2-1
def scrn21y(y):
	return (y / SCREEN_Y)*-2+1	#Hoo Ra

def readImage():
	global frame
	if frame is None:
		return []	#Abandon all hope ye who enter here
	
	#ret, frame = cap.read() #gets frame from camera
	#frame = cv2.blur(frame, (7,7))

	g_in = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #returns frame in black and white
	g_mask = cv2.inRange(g_in, lower_g, upper_g) #returns where certain color is shown
	g_res = cv2.bitwise_and(frame, frame, mask= g_mask)

	kernel = np.ones((5,5), np.uint8)
	g_thresh = cv2.dilate(g_mask, kernel, iterations = DILATE_ITERATIONS)
	g_thresh = cv2.erode(g_thresh, kernel, iterations = ERODE_ITERATIONS) #removes random noise for cleaner image
	image, contours, hierarchy = cv2.findContours(g_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #returns image with outlined color

	rects = []
	areas = []
	for i in contours:
		rect = cv2.minAreaRect(i) #takes a contour and puts a box around it
		rects.append(rect)
		area = rect[1][0]*rect[1][1]
		areas.append(area)
	actl = sorted(zip(rects, areas, contours), key=lambda x: x[1], reverse=True)
	
	return actl

def capImage():
	global frame
	while True:
		ret, frame = cap.read() #gets frame from camera



def shootDistance_calculate(mid_y):
	theta = FOV_Y / 2 * mid_y + REF_THETA
	distance = (REF_TOW_H - REF_CAM_H) / math.tan(math.radians(theta))
	return theta, distance
def readDistanceShooter():
	cl = readImage()
	if( len(cl) > 0):
		global data

		topmost = scrn21y(tuple(cl[0][2][cl[0][2][:,:,1].argmin()][0])[1])	#I don't know how this works
		bottommost = scrn21y(tuple(cl[0][2][cl[0][2][:,:,1].argmax()][0])[1]) #but the arrays are 4 deep
		mid_x = scrn21x(cl[0][0][0][0])	#i know right

		theta1, distance1 = shootDistance_calculate(topmost)
		theta2, distance2 = shootDistance_calculate(bottommost)

		data = [mid_x, scrn21y(cl[0][0][0][1]), (theta1+theta2)/2, (distance1+distance2)/2]

def readDistanceGears():
	global data
	cl = readImage()
	if( len(cl) == 0):
		return
	elif len(cl) == 1:
		mid_x = scrn21x(cl[0][0][0][0])
	else:
		mid_x = (scrn21x(cl[0][0][0][0]) + scrn21x(cl[1][0][0][0]))/2
	data = [mid_x, 0, 0, -42]	#don't use

CamState = "Shooter"	#vidcap default is 0
SwitchState = False
def readDistance():
	global CamState, SwitchState, cap
	if SwitchState != False:
		print("reset")
		global data
		data = ["", "", "", ""]
		if SwitchState == "Gears":
			cap = cv2.VideoCapture(1)
			CamState = "Gears"
		else:
			cap = cv2.VideoCapture(0)
			CamState = "Shooter"
		SwitchState = False
	if CamState == "Shooter":
		readDistanceShooter()
	else:
		readDistanceGears()
		

def readDistanceCaller():
	while True:
		readDistance()

def checkGet():
	while True:
		global ser
		ans = ser.readline()
		if ans:
			global data, SwitchState, CamState
			if ans.decode() == "shooter\n" and CamState != "Shooter":
				SwitchState = "Shooter"
				ser.write("Affirmative\n".encode())
				print("switching")
			elif ans.decode() == "gears\n" and CamState != "Gears":
				SwitchState = "Gears"
				ser.write("Affirmative\n".encode())
				print("switching")
			else:
				ser.write(("sm" + str(data[0]) + "m" + str(data[1]) + "m" + str(data[2]) + "m" + str(data[3]) + "e\n").encode())

def main():
	threadArray = []

	capThread = FuncThread(capImage)
	capThread.setDaemon(True)
	capThread.start()
	threadArray.append(capThread)
		
	readThread = FuncThread(readDistanceCaller)
	readThread.setDaemon(True)
	readThread.start()
	threadArray.append(readThread)

	chkThread = FuncThread(checkGet)
	chkThread.setDaemon(True)
	chkThread.start()
	threadArray.append(chkThread)

	for thread in threadArray:
 		thread.join()


main()
