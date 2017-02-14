#Will your code should be at the bottom. Fill in the stuff in HooBoyShoot. Also I think the calls to AutonTankDrive are wrong.

import math
import serial

DDZ_ROT = 0.06
MIN_ROT_SPD = 0.01
MAX_ROT_SPD = 0.2

DDZ_MOV = 0.1
MIN_MOV_SPD = 0.05

REF_DIST = 2 	#CHANGE -- equal to distance at which the tower tape is in the dead middle of the camera's view
		#Should be findable from REF_THETA and REF_CAM_H in the Pi file

REF_CHNG_H = 1.9	#CHANGE 

MUZZLE_VELOCITY = 30	#meters/second
COMPLETELY_ARBITRARY_CONSTANT = 1

class Tthhinnggyy:
	mid_x = None
	mid_y = None
	theta = None
	distance = None
	ser = None

	def __init__(self):
		self.ser = serial.Serial("/dev/ttyS1", 115200, timeout=1)

	def receive(self):
		self.ser.write("hoo boy, waffles\n")
		ans = self.ser.readLine()
		ans = ans.decode()
		return ans

	def decode(self, string):
		stuff = []
		number = ""
		state = "previous"
		for char in string:
			if state == "previous":
				if char == "s":
					state = "start"
			elif state == "start":
				if char == "m":
					state = "read"
			elif state == "read":
				if char == "m":
					stuff.append(number)
					number = ""
				elif char == "e":
					stuff.append(number)
					number = ""
					state == "previous"
				else:
					number += char
		return stuff

	def centerSide(self):
		if(math.abs(self.theta) <= DDZ_ROT):	#radians, arbitrary deadzone value
			spd = max(MIN_ROT_SPD, min(MAX_ROT_SPD, math.abs(self.theta)))*math.copysign(1.0, self.theta)	#again arbitrary numbers
			self.autonTankDrive(spd, -spd)
			return False
		return True

	def centerLine(self):
		distance -= REF_DIST
		if(math.abs(self.distance) <= DDZ_MOV):	#meters, arbitrary deadzone value
			spd = max(MIN_MOV_SPD, math.abs(self.distance))*math.copysign(1.0, self.distance)
			self.autonTankDrive(spd,spd)
			return False
		return True

	def HooBoyShoot(self):
		pass
		#MAGIC -- call a function that spins the shooting wheels


thng = Tthhinnggyy()
thng.receive()


'''	def ShootDistance(self):	#I *guarantee* this does *not* work
		angle = math.arcsin((REF_CHNG_H/self.distance+4.9*self.distance)/MUZZLE_VELOCITY)
		#MAGIC -- set the shooting apparatus angle
		#MAGIC -- call a function that spins the shooting wheels

		#note that this function may not work on the grounds of returning angles beyond our operational capabilities
		#it can be changed, but it's not important anyway
'''
'''
if centerSide() and centerLine() :	#this works because of short-circuiting
	HooBoyShoot()
'''

