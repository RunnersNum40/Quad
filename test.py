from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
for x in range(16):
		kit.servo[x].set_pulse_width_range(450, 2450)

while True:
	kit.servo[0].angle = 180
	kit.servo[1].angle = 0
	sleep(1)
	kit.servo[0].angle = 0
	kit.servo[1].angle = 180
	sleep(1)