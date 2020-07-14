from time import sleep
from adafruit_servokit import ServoKit

def angles(kit, angle):
	for x in range(16):
		kit.servo[x].angle = angle

kit = ServoKit(channels=16)
for x in range(16):
		kit.servo[x].set_pulse_width_range(450, 2450)


try:	
	v = 1
	while True:
		sleep(1)
		angles(kit, 180*v)
		v = 1-v

finally:
	angles(kit, 90)