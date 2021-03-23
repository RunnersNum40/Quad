from leg import Leg
from servos import Servos
from time import sleep
from configurer import Config

class Quad:
    def __init__(self, config_file):
        self.config = Config()
        self.config.read_config(config_file)
        self.servos = Servos(16, self.config.mimimum_pulse, self.config.maximum_pulse, self.config.kill_angle, self.config.angle_offsets)

        legs = []
        for i in range(4):
            leg_config = self.config["leg"+str(i+1)]
            leg = Leg(leg_config["quadrants"], leg_config["positions"])
            leg.servos(*(self.servos[x] for x in leg_config["servo_pins"]))
            leg.limbs(*leg_config["limb_lengths"])
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
