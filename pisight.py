import cv2
import numpy as np
import math
import serial
import threading
from time import sleep
from time import time

# Set to 1 to print output to the screen
# Set to 0 to print output to the serial port
DEBUG_MODE = 0
DEBUG_PRINT = 10
capId = 0
lastCapId = 0
frameCounter = 0

class MockSerial:
	lastCapId = 0
	lastFrameTime = 0
	
	def readline(self):
		global capId
		if self.lastCapId != capId:
			self.lastFrameTime = capId - self.lastCapId
			self.lastCapId = capId
			return True
		return False
		
	def write(self, data):
		fps = 1 / self.lastFrameTime
		print(str(fps) + "fps / " + str(self.lastFrameTime*1000) + "ms: " + data.decode())

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
	return (y / SCREEN_Y)*-2+1

def readImage():
	global capId
	global lastCapId
	global DEBUG_PRINT
	global frameCounter
	global frame
	
	if frame == None:
		return []
	
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
	capId = time()
	frameTime = capId - lastCapId
	lastCapId = capId
	frameCounter += 1
	
	if DEBUG_PRINT and frameCounter % DEBUG_PRINT == 0:
		print(str(frameTime) + "/" + str(1/frameTime) + "\n")
	
	return actl

def shootDistance_calculate(mid_y):
	theta = FOV_Y / 2 * mid_y + REF_THETA
	distance = (REF_TOW_H - REF_CAM_H) / math.tan(math.radians(theta))
	return theta, distance
'''def shootDistance_print(mid_x, mid_y, theta, distance):
	print("mid_x" + str(mid_x))
	print("mid_y" + str(mid_y))
	print("theta" + str(theta))
	print("Dist:" + str(distance),end="\n")'''
def readDistance(): 
	pass
def readDistanceShooter():
	while(True):
		cl = readImage()
		if( len(cl) > 0):
			global data

			topmost = scrn21y(tuple(cl[0][2][cl[0][2][:,:,1].argmin()][0])[1])	#I don't know how this works
			bottommost = scrn21y(tuple(cl[0][2][cl[0][2][:,:,1].argmax()][0])[1]) #but the arrays are 4 deep
			mid_x = scrn21x(cl[0][0][0][0])	#i know right

			theta1, distance1 = shootDistance_calculate(topmost)
			theta2, distance2 = shootDistance_calculate(bottommost)

			data = [mid_x, scrn21y(cl[0][0][0][1]), (theta1+theta2)/2, (distance1+distance2)/2]
		#else:
		#	print("", end=".", flush=True)
def readDistanceGears():
	mid_x = (scrn21x(cl[0][0][0][0]) + scrn21x(cl[1][0][0][0]))/2
	data = [mid_x, 0, 0, 0]	#don't use mid_y, theta, distance
	#strafe instead

def capImage():
	global frame
	while True:
		ret, frame = cap.read() #gets frame from camera

readDistance = readDistanceShooter
def switch():
		if readDistance == readDistanceShooter:
			readDistance = readDistanceGears
		else:
			readDistance = readDistanceShooter
		
		
def checkGet():
	while True:
		global ser
		ans = ser.readline()
		if ans:
			global data
			if ans.decode() == "the times they are\n":
				switch()
			else:
				#print("transmit")
				ser.write(("sm" + str(data[0]) + "m" + str(data[1]) + "m" + str(data[2]) + "m" + str(data[3]) + "e\n").encode())

def main():
        threadArray = []

        capThread = FuncThread(capImage)
        capThread.setDaemon(True)
        capThread.start()
        threadArray.append(capThread)
		
        readThread = FuncThread(readDistance)
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
#input("stop?")



'''for i in cl:
		for j in cl:
			if (i == j):
				continue
			if abs(i[0][1] - j[0][1] - 0.1016) <= 0.1016 and abs(i[1][0] - j[1][0]) <= 0.2:
				return i, j

code for checking that they really are the tower vision tape'''

'''
			#mid_x = scrn21x(cl[0][0][0][0] + cl[0][0][1][0]/2)
			#mid_y = -1*scrn21y(cl[0][0][0][1] + cl[0][0][1][1]/2)
			#Reversed -count from top, not bottom
'''

'''if(abs(mid_x) >= SMALL_VAL):
	print("mid_x" + str(mid_x))
	turn(mid_x * FOV_X / 2)
	continue
'''
