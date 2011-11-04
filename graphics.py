from panda3d.core import AntialiasAttrib
from pandac.PandaModules import WindowProperties, Vec3

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
        base.camLens.setNearFar(1, 1024)
        self.camera_target = (0, 0, 0)
        taskMgr.add(self._camera_task, "Camera")

    def _camera_task(self, task):
        move = self.camera_target.getPos() + Vec3(0, -10, 3) - base.camera.getPos()
        base.camera.setPos(base.camera.getPos() + move * globalClock.getDt() * .5)
        base.camera.lookAt(self.camera_target)
        return task.cont
