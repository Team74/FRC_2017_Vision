#Will your code should be at the bottom. Fill in the stuff in HooBoyShoot. Also I think the calls to AutonTankDrive are wrong.

import math
import serial
from time import sleep

DDZ_ROT = 4#0.06
MIN_ROT_SPD = 0.01
MAX_ROT_SPD = 0.2

DDZ_MOV = 0.1
MIN_MOV_SPD = 0.05

REF_THETA = 40
REF_TOW_H = 1.9
REF_CAM_H = 0
REF_DIST = (REF_TOW_H - REF_CAM_H) / math.tan(REF_THETA)	

MUZZLE_VELOCITY = 30	#meters/second
COMPLETELY_ARBITRARY_CONSTANT = 1

class Tthhinnggyy:
	mid_x = None
	mid_y = None
	theta = None
	distance = None
	ser = None

	def __init__(self):
		self.ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.05)

	def autonTankDrive(self, l, r):
		print("turn\t" + str(l) + "\t" str(r))

	def receive(self):
		self.ser.write("boom ya got waffles\n".encode())
		ans = self.ser.readline()
		if ans:
			ans = self.uncode(ans.decode())
			self.mid_x = float(ans[0])
			self.mid_y = float(ans[1])
			self.theta = float(ans[2])
			self.distance = float(ans[3])
		#print(str(self.mid_x) + "\t" + str(self.mid_y) + "\t" + str(self.theta) + "\t" + str(self.distance))

	def uncode(self, string):
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
		if(abs(self.theta - REF_THETA) > DDZ_ROT):	#radians, arbitrary deadzone value
			spd = math.copysign(0.2, self.theta)	#again arbitrary numbers
			self.autonTankDrive(spd, -spd)
			return False
		return True

	def centerLine(self):
		if(abs(distance - REF_DIST) > DDZ_MOV):	#meters, arbitrary deadzone value
			spd = copysign(0.1, distance)#max(MIN_MOV_SPD, abs(distance))*math.copysign(1.0, distance)
			self.autonTankDrive(spd,spd)
			return False
		return True


#max(MIN_ROT_SPD, min(MAX_ROT_SPD, abs(self.theta - REF_THETA)))
'''	def ShootDistance(self):	#I *guarantee* this does *not* work
		angle = math.arcsin(((REF_TOW_H - REF_CAM_H)/self.distance+4.9*self.distance)/MUZZLE_VELOCITY)
		#MAGIC -- set the shooting apparatus angle
		#MAGIC -- call a function that spins the shooting wheels

		#note that this function may not work on the grounds of returning angles beyond our operational capabilities
		#it can be changed, but it's not important anyway
'''
'''
thng.receive()
if thng.centerSide() and thng.centerLine() :	#this works because of short-circuiting
	HooBoyShoot()
'''

