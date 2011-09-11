from panda3d.core import CardMaker
from pandac.PandaModules import OdeBoxGeom, Vec3

class Plate:

    def __init__(self, level, x, y, z, width, height, factor_x, factor_y):         
        
        self.model = loader.loadModel("cube")
        self.model.reparentTo(render)
        self.model.setScale(width, height, 0.2)          
        self.model.setPos(x, y, z)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(0.7, 0.3, 0.1, 1)
        self.model.setTexture(loader.loadTexture('maps/noise.rgb'))
                 
        self.level = level
        self.width = width
        self.height = height        
        self.factor_x = factor_x
        self.factor_y = factor_y
        
        taskMgr.add(self._move_task, "PlateMoveTask")

    
    def _move_task(self, task):
        self.model.setHpr(0,
                          -self.level.smooth_y * self.factor_y,
                          self.level.smooth_x * self.factor_x)   
        self.geom.setPosition(self.model.getPos())                     
        self.geom.setQuaternion(self.model.getQuat())
        return task.cont

    def enable_physics(self, physics):
        self.geom = OdeBoxGeom(physics.space, self.width, self.height, 0.2)
