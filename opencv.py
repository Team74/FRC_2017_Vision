import cv2
import numpy as np
import math


SCREEN_X = 640
SCREEN_Y = 480
SMALL_VAL = 0.1	#magic number 1
FOV_X = 61		#pulled from online? Mostly a guess
FOV_Y = 34
REF_THETA = 40	#SPECIFY		#angle the camera is mounted
REF_TOW_H = 1.9
REF_CAM_H = 0#.85 #SPECIFY		#height of camera on the robot above the ground

cap = cv2.VideoCapture(0)

cv2.namedWindow("d")

lower_g = np.array([65, 100, 100])
upper_g = np.array([85, 255, 255])

def turn(theta):
	print("turn " + str(theta) + " degrees")
	input("yo")

def scrn21x(x):
	return (x / SCREEN_X)*2-1
def scrn21y(y):
	return (y / SCREEN_Y)*2-1

def readImage():
	ret, frame = cap.read() #gets frame from camera
	#frame = cv2.blur(frame, (7,7))

	g_in = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #returns frame in black and white
	g_mask = cv2.inRange(g_in, lower_g, upper_g) #returns where certain color is shown
	g_res = cv2.bitwise_and(frame, frame, mask= g_mask)

	kernel = np.ones((5,5), np.uint8)
	g_thresh = cv2.dilate(g_mask, kernel, iterations = 3)
	g_thresh = cv2.erode(g_thresh, kernel, iterations = 3) #removes random noise for cleaner image
	image, contours, hierarchy = cv2.findContours(g_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #returns image with outlined color

	cv2.imshow("d",frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		quit()

	rects = []
	areas = []
	for i in contours:
		rect = cv2.minAreaRect(i) #takes a contour and puts a box around it
		rects.append(rect)
		area = rect[1][0]*rect[1][1]
		areas.append(area)
	actl = sorted(zip(rects, areas, contours), key=lambda x: x[1], reverse=True)
	return actl

def shootDistance():

	mid_x = SMALL_VAL
	while(True):
		cl = readImage()

		if( len(cl) > 0):

			#mid_x = scrn21x(cl[0][0][0][0] + cl[0][0][1][0]/2)
			#mid_y = -1*scrn21y(cl[0][0][0][1] + cl[0][0][1][1]/2)
			#Reversed -count from top, not bottom

			topmost = tuple(cl[0][2][cl[0][2][:,:,1].argmin()][0])
			bottommost = tuple(cl[0][2][cl[0][2][:,:,1].argmax()][0])

			mid_x = scrn21x(topmost[0])
			mid_y = -1*scrn21y(topmost[1])

			'''if(abs(mid_x) >= SMALL_VAL):
				print("mid_x" + str(mid_x))
				turn(mid_x * FOV_X / 2)
				continue
			'''
			theta = FOV_Y / 2 * mid_y + REF_THETA
			distance = (REF_TOW_H - REF_CAM_H) / math.tan(math.radians(theta))
			#magically turn distance into wheel speed for shooting
			print("mid_x" + str(mid_x))
			print("mid_y" + str(mid_y))
			print("theta" + str(theta))
			print("Dist:" + str(distance),end="\n")

			mid_x = scrn21x(bottommost[0])
			mid_y = -1*scrn21y(bottommost[1])

			theta = FOV_Y / 2 * mid_y + REF_THETA
			distance = (REF_TOW_H - REF_CAM_H) / math.tan(math.radians(theta))
			#magically turn distance into wheel speed for shooting
			print("mid_x" + str(mid_x))
			print("mid_y" + str(mid_y))
			print("theta" + str(theta))
			print("Dist:" + str(distance),end="\n")

			print("\n\n")

			return distance
		else:
			print("", end=".", flush=True)


def main():
	while True:
		shootDistance()
main()

'''for i in cl:
		for j in cl:
			if (i == j):
				continue
			if abs(i[0][1] - j[0][1] - 0.1016) <= 0.1016 and abs(i[1][0] - j[1][0]) <= 0.2:
				return i, j

code for checking that they really are the tower vision tape'''
