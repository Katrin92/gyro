from panda3d.core import AntialiasAttrib
from pandac.PandaModules import WindowProperties, Vec3, Mat3

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
        self._camera_rotate = 0.0
        self._camera_smooth = Vec3(0, 0, 0)
        taskMgr.add(self._camera_task, "Camera")

    def _camera_task(self, task):
        self._camera_rotate += (self.camera_target.controls.view_rotation -
                                self._camera_rotate) * globalClock.getDt() * 10
        self._camera_smooth += (self.camera_target.model.getPos() -
                                self._camera_smooth) * globalClock.getDt()

        base.camera.setPos(self._camera_smooth +
                           Mat3.rotateMat(self._camera_rotate).
                           xform((-10, 0, 3)))

        base.camera.lookAt(self.camera_target.model)

        return task.cont
