from level import Level
from plate import Plate
from obstacle import Obstacle

class ObstacleWall(Level):

    _h = -1

    def __init__(self):
        Level.__init__(self)
        self._init_plates()
        self._init_obstacles()

    def _init_plates(self):
        self.objects = [Plate(self,    -9,  0,     -.3,  5.5,  4),
                        Plate(self, -5.75,  0, self._h,    1, 10),
                        Plate(self,  -2.5,  0,    -1.5,  5.5,  6)]

    def _init_obstacles(self):
        for z in range(5):
            for y in range(5 - z):
                self.objects.append(Obstacle(-5.75, -2.4 + y*1.2 + 0.6*z, z + 0.6 + self._h))
