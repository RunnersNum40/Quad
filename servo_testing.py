from servos import Servos

servos = Servos(num=16, mimimum_pulse=450, maximum_pulse=2450, kill_angle=90)
servo = servos[int(input("What servo: "))]
x = input("What angle: ")
while x != "end":
    try:
        servo.angle = float(x)
    except ValueError:
        print("Must input a number")
    x = input("New angle: ")