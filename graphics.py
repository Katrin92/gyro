from panda3d.core import AntialiasAttrib
from pandac.PandaModules import WindowProperties

class Graphics:

    def __init__(self):
        self._init_graphics()
        self._init_camera()

    def _init_graphics(self):
        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        base.setFrameRateMeter(True)
        render.setShaderAuto()
        render.setAntialias(AntialiasAttrib.MAuto)

    def _init_camera(self):
        base.camLens.setNearFar(1, 100)
        self.camera_target = (0, 0, 0)
        taskMgr.add(self._camera_task, "Camera")

    def _camera_task(self, task):
        base.camera.setPos(0, -30, 20)
        base.camera.lookAt(self.camera_target)
        return task.cont
