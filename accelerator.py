from pandac.PandaModules import OdeCylinderGeom, Vec3
from pandac.PandaModules import TransparencyAttrib, BitMask32, Texture

class Accelerator:

    def __init__(self, x, y, z):

        self.model = loader.loadModel("circle")
        self.model.reparentTo(render)
        self.model.setPos(x, y, z)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(1, 1, 1, 1)
        self.model.setTexture(loader.loadTexture('textures/spiral.png'))

        self.glow = loader.loadModel("tube")
        self.glow.reparentTo(render)
        self.glow.setShaderOff()
        self.glow.setLightOff()
        self.glow.hide(BitMask32.allOn())
        self.glow.show(BitMask32(0x01))
        self.glow.setPos(x, y, z + 0.05)
        self.glow.setHpr(0, 0, 0)
        self.glow.setColor(1, 1, 1, 1)
        texture = loader.loadTexture('textures/green_glow.png')
        texture.setWrapU(Texture.WMClamp)
        texture.setWrapV(Texture.WMClamp)
        self.glow.setTexture(texture)
        self.glow.setTransparency(TransparencyAttrib.MAlpha)
        self._active = False
        self.visibility = 0

        taskMgr.add(self._update_task, "AcceleratorUpdateTask")

    def enable_physics(self, physics):
        self.geom = OdeCylinderGeom(physics.space, 1.5, 0.1)
        self.geom.setPosition(self.model.getPos())
        self.geom.setQuaternion(self.model.getQuat())
        physics.actions.append(self._deactivate)

    def _deactivate(self):
        self._active = False

    def _update_task(self, task):
        if self._active:
            self.visibility = min(1, self.visibility + globalClock.getDt())
        else:
            self.visibility = max(0, self.visibility - globalClock.getDt()*2)
        self.glow.setAlphaScale(self.visibility)
        return task.cont

    def player_interact(self, player):
        distance = (player.model.getPos().getXy()-
                    self.model.getPos().getXy()).length()
        if distance < .3:
            self._active = True
            return True
        else:
            return False

    def reset(self):
        pass
