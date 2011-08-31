from direct.showbase.ShowBase import ShowBase

from graphics import Graphics
from player import Player
from environment import Environment
from physics import Physics

class GyroApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.graphics = Graphics()
        self.environment = Environment()
        self.player = Player()
        self.physics = Physics()

        self.graphics.camera_target = (0, 0, 0)
        self.environment.spotlight_target = self.player.model

        self.player.model.setPos(-5, 0, 1)

        self.environment.enable_physics(self.physics)
        self.player.enable_physics(self.physics)

if __name__ == '__main__':
    app = GyroApp()
    app.run()
