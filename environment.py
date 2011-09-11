from panda3d.core import Spotlight, AmbientLight, VBase4

class Environment:

    def __init__(self):
        self._init_ambient()
        self._init_spotlight()

    def _init_ambient(self):
        self.ambient = render.attachNewNode(AmbientLight('alight'))
        self.ambient.node().setColor(VBase4(0.3, 0.3, 0.3, 3))
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
        self.spotlight.setPos(0, 0, 20)
        self.spotlight.lookAt(self.spotlight_target)
        return task.cont


                                         
                                         
