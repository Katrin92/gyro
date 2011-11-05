from panda3d.core import Vec4
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectWaitBar

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

        self.health_bar = DirectWaitBar(pos = (0, 0, -0.9), scale = 0.5,
                                        frameColor = Vec4(0.3, 0.3, 0.3, 0.8),
                                        relief = 5, borderWidth = (0.05,0.05))
        self.health_bar.setBillboardPointEye()
        self.health_bar.reparentTo(aspect2d)
        self.health_bar.setShaderOff()
        self.max_health = self.player.health
        taskMgr.add(self.update_health, "UpdateHealthTask")

        self.accept("escape", self.reset)

    def update_health(self, task):
        value = self.player.health / self.max_health
        self.health_bar['value'] = 100 * value
        self.health_bar['barColor'] = Vec4(1 - value, value, 0, 0.8)
        return task.cont

    def reset(self):
        self.player.reset()

if __name__ == '__main__':
    app = GyroApp()
    app.run()
