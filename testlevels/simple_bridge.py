from level import Level
from plate import Plate

class SimpleBridge(Level):

    def __init__(self):
        Level.__init__(self)
        self._init_plates()

    def _init_plates(self):
        self.objects = (Plate(self, -10, 0, -0.5,  4,   4),
                        Plate(self,   0, 0, -1.5, 16, 2.5),
                        Plate(self,  10, 0, -2.5,  4,   4))
