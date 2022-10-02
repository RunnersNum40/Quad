from math import asin, acos, atan2, sqrt, degrees
import warnings

class Leg:
    """The leg class contains the inverse kinematics solver for a 3 DOF leg"""
    def __init__(self, quadrant, position):
        self.quadrant = quadrant
        self.offsets = position

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def set_limb_legths(self, coxa, femur, tibia):
        """Set the limb lengths"""
        self.coxa = coxa
        self.femur = femur
        self.tibia = tibia

    def set_servos(self, hip, knee, ankle):
        """Pass the servo objects"""
        self.hip = hip
        self.knee = knee
        self.ankle = ankle

    def __len__(self):
        return sqrt(self.x**2+self.y**2+self.z**2)

    @property
    def pos(self):
        return (self.x, self.y, self.z)

    def set(self, x, y, z):
        self.x, self.y, self.z = (cord-offset for cord, offset in zip((x, y, z), self.offsets))

        f = sqrt(self.x**2+self.y**2)-self.coxa #distance from the edge of the coaxa to the foot excluding the z direction
        d = sqrt(f**2+self.z**2) #distance from the edge of the coaxa to the foot

        print(f"Leg solving: ({self.x}, {self.y}, {self.z})\n\tf: {f}mm,   d: {d}mm")

        b1 = acos(f/d)
        b2 = acos((self.femur**2+d**2-self.tibia**2)/(2*self.femur*d))

        print(f"\tb1: {degrees(b1)},   b2: {degrees(b2)}")

        h = degrees(atan2(self.x, self.y))%360
        k = degrees(b2-b1)%360
        a = degrees(acos((self.femur**2+self.tibia**2-d**2)/(2*self.femur*self.tibia)))%360

        print(f"\tHip: {h},   Knee: {k},   Ankle: {a}")

        self.hip.angle = h*self.quadrant[0]
        self.knee.angle = k*self.quadrant[1]
        self.ankle.angle = a*self.quadrant[2]