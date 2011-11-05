from level import Level
from plate import Plate

class SimpleBridge(Level):

    def __init__(self):
        Level.__init__(self)
        self._init_plates()

    def _init_plates(self):
        self.objects = (Plate(-10, 0, -0.5,  4,   4),
                        Plate(  0, 0, -1.5, 16, 2.5),
                        Plate( 10, 0, -2.5,  4,   4))
