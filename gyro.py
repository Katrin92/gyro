from direct.showbase.ShowBase import ShowBase

from graphics import Graphics
from environment import Environment
from level import Level
from player import Player
from physics import Physics

class GyroApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.graphics = Graphics()
        self.environment = Environment()
        self.level = Level()
        self.player = Player()
        self.physics = Physics()

        self.graphics.camera_target = self.player.model
        self.environment.spotlight_target = self.player.model

        self.player.model.setPos(-10, 0, 1)

        self.level.enable_physics(self.physics)
        self.player.enable_physics(self.physics)
        
        self.accept("space", self.reset)
    
    def reset(self):
        self.player.reset()
        self.level.reset()

if __name__ == '__main__':
    app = GyroApp()
    app.run()
