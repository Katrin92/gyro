from direct.showbase.ShowBase import ShowBase

from graphics import Graphics
from environment import Environment
from player import Player
from physics import Physics

import testlevels

class GyroApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.graphics = Graphics()
        self.environment = Environment()
        self.physics = Physics()

        #self.level = testlevels.SimpleBridge()
        self.level = testlevels.ObstacleWall()
        self.level.enable_physics(self.physics)

        self.player = Player(self.level)
        self.player.model.setPos(-10, 0, 1)
        self.player.enable_physics(self.physics)

        self.graphics.camera_target = self.player.model
        self.environment.spotlight_target = self.player.model

        self.accept("escape", self.reset)

    def reset(self):
        self.player.reset()

if __name__ == '__main__':
    app = GyroApp()
    app.run()
