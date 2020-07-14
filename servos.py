from adafruit_servokit import ServoKit
from time import sleep

def is_number(n):
	"""Tests if the provided value can be treted as a number"""
	try:
		n+1
		1+n
		return True
	except ValueError:
		return False



class Servos:
	def __init__(self, num=16, mimimum_pulse=450, maximum_pulse=2450, kill_angle=90):
		self.kill_angle = kill_angle
		self.kit = ServoKit(channels=16)
		self.servos = [Servo(self.kit.servo[x], x) for x in range(16)]
		for servo in self.servos:
			servo.kit_servo.set_pulse_width_range(mimimum_pulse, maximum_pulse)

	def set(self, angle):
		for servo in self.servos:
			servo.angle = angle

	def __iter__(self):
		return self.servos.__iter__()

	def __getitem__(self, index):
		return self.servos[index]

	def __del__(self):
		"""When the program ends set all servos to a predefined position to ensure replicable behavior when progam is not running"""
		self.set(self.kill_angle)



class Servo:
	def __init__(self, kit_servo, num):
		self.kit_servo = kit_servo
		self.num = num
		self._angle = None
		self.wait = False #if True the servo will wait until it has rotated to the desired location before letting code resume

	@property
	def angle(self):
		if self._angle is None:
			raise Exception("Servo angle requested before being set, servo {}".format(self.num))
		else:
			return self._angle

	@angle.setter
	def angle(self, new_angle):
		if not is_number(new_angle):
			raise Exception("Angle assigments must be numbers, {} is not a valid assignment".format(repr(new_angle)))
		elif not 0<=new_angle<=180:
			raise Exception("Servo angles must be between 0 and 180 degrees, {} is not a valid assignment".format(new_angle))
		else:
			self._angle = new_angle
			self.kit_servo.angle = self._angle
			if self.wait:
				sleep(0.002667*abs(self._angle-new_angle))