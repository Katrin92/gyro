from panda3d.core import CardMaker, Spotlight, AmbientLight, VBase4, NodePath
from pandac.PandaModules import OdePlaneGeom, Vec4
import math

class Environment:

    def __init__(self):
        self._init_ground()
        self._init_ambient()
        self._init_spotlight()
        self._init_mouse()

    def _init_ground(self):
        cmaker = CardMaker("ground")
        cmaker.setFrame(-10, 10, -10, 10)
        floor = render.attachNewNode("floor")
        floor.setHpr(0, -90, 0)
        self.ground = floor.attachNewNode(cmaker.generate())
        self.ground.setPos(0, 0, 0)        
        self.ground.setHpr(0, 0, 0)
        self.ground.setColor(0.7, 0.1, 0.1, 1)
        self.ground.setTexture(loader.loadTexture('maps/noise.rgb'))

    def _init_ambient(self):
        self.ambient = render.attachNewNode(AmbientLight('alight'))
        self.ambient.node().setColor(VBase4(0.1, 0.1, 0.1, 1))
        render.setLight(self.ambient)

    def _init_spotlight(self):
        self.spotlight = render.attachNewNode(Spotlight('light'))
        self.spotlight.node().setScene(render)
        self.spotlight.node().setColor(VBase4(0.8, 0.8, 0.8, 1))
        self.spotlight.node().setShadowCaster(True, 1024, 1024)
        self.spotlight.node().getLens().setNearFar(1, 50)
        self.spotlight.node().getLens().setFov(40)
        render.setLight(self.spotlight)

        self.spotlight_target = (0, 0, 0)
        taskMgr.add(self._spotlight_task, "SpotlightTask")

    def _spotlight_task(self, task):
        self.spotlight.setPos(5, -5, 5)
        self.spotlight.lookAt(self.spotlight_target)
        return task.cont

    def _init_mouse(self):
        taskMgr.add(self._mouse_task, "MouseTask")
        self.x = 0
        self.y = 0
        
    def _mouse_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            x=base.mouseWatcherNode.getMouseX() * 30
            y=base.mouseWatcherNode.getMouseY() * 30
            self.x += (x - self.x) * globalClock.getDt() * 0.2  
            self.y += (y - self.y) * globalClock.getDt() * 0.2        
            self.ground.setHpr(self.x, -self.y, 0)
            up = self.ground.getQuat().getForward()
            self.geom.setParams(-up.x, -up.z, up.y, 0)
        return task.cont            

    def enable_physics(self, physics):
        self.geom = OdePlaneGeom(physics.space, Vec4(0, 0, 1, 0))
                                         
                                         
