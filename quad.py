from leg import Leg
from servos import Servos
from time import sleep
from config_reader import read

class Quad:
    def __init__(self, config_file):
        config = read(config_file)
        self.servos = Servos(16, config.mimimum_pulse, config.maximum_pulse, config.kill_angle, config.angle_offsets)

        legs = []
        for i in range(4):
            leg_config = config["leg"+str(i+1)]
            leg = Leg(leg_config["quadrants"], leg_config["positions"])
            leg.set_servos(*(self.servos[x] for x in leg_config["servo_pins"]))
            leg.set_limb_legths(*leg_config["limb_lengths"])
            legs.append(leg)

        self.leg0, self.leg1, self.leg2, self.leg3 = legs

    def __getitem__(self, index):
        return self.legs[index]

    @property
    def legs(self):
        return (self.leg0, self.leg1, self.leg2, self.leg3)

if __name__ == '__main__':
    q = Quad("quad.config")
    q[0].set(150, 100, 150)
    sleep(3)
    q[0].set(150, -100, 150)
    sleep(3)
    q[0].set(150, 0, 150)
    sleep(3)
