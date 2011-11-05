from level import Level
from plate import Plate
from obstacle import Obstacle

import math

class Staircase(Level):

    def __init__(self):
        Level.__init__(self)
        self._init_plates()
        self._init_obstacles()

    def _init_plates(self):
        self.objects = []
        for z in range(18):
            plate = Plate(-10.0 * math.cos(z*math.pi/9),
                          10.0 * math.sin(z*math.pi/9),
                          -0.3 + z * 0.5,  3,  3)
            self.objects.append(plate)

    def _init_obstacles(self):
        for z in range(9):
            box1 = Obstacle(-10.0 * math.cos((z+0.5)*math.pi/4.5),
                             10.0 * math.sin((z+0.5)*math.pi/4.5), 0.8 + z)
            box2 = Obstacle(-10.0 * math.cos((z+0.5)*math.pi/4.5),
                             10.0 * math.sin((z+0.5)*math.pi/4.5), 1.8 + z)
            self.objects.append(box1)
            self.objects.append(box2)
