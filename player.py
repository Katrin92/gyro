from panda3d.core import VBase3
from pandac.PandaModules import OdeBody, OdeMass
from pandac.PandaModules import OdeTriMeshData, OdeTriMeshGeom

class Player:

    def __init__(self):
        self._init_model()
        self._init_controls()

    def _init_model(self):
        self.model = loader.loadModel("gyro")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 2)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(0.1, 0.7, 0.7, 1)
        self.model.setTexture(loader.loadTexture('maps/noise.rgb'))

    def _init_controls(self):
        self.controls = Controls()

    def enable_physics(self, physics):
        self.body = OdeBody(physics.world)
        self.body.setPosition(self.model.getPos(render))
        self.body.setQuaternion(self.model.getQuat(render))
        self.body.setAngularVel(0, 0, 30)

        mass = OdeMass()
        mass.setCylinder(10, 2, 1.0, 0.5)
        self.body.setMass(mass)

        modelTrimesh = OdeTriMeshData(loader.loadModel("gyro-low"), True)
        modelGeom = OdeTriMeshGeom(physics.space, modelTrimesh)
        modelGeom.setBody(self.body)

        physics.bodymodels[self.body] = self.model
        physics.actions.append(self._stabilize)
        physics.actions.append(self._move)

    def _stabilize(self):
        avel = self.body.getAngularVel()
        rot = self.body.getRotation()
        corr = rot.xformVec(VBase3(0, 0, 1))
        self.body.addTorque((corr.y*-50 - avel.x*50)*abs(avel.z),
                            (corr.x* 50 - avel.y*50)*abs(avel.z), 0)

    def _move(self):
        avel = self.body.getAngularVel()
        if self.controls.accelerating and avel.z < 30:
            self.body.addRelTorque(0, 0, 50)
        x, y = self.controls.direction
        self.body.addForceAtRelPos(x*10*(abs(avel.z)+5),
                                   y*10*(abs(avel.z)+5),
                                   0, 0, 0, -0.3)



class Controls:

    def __init__(self):
        self.accelerateStop()
        self.stop()

        base.accept('space', self.accelerate)
        base.accept('space-up', self.accelerateStop)

        base.accept('arrow_left', self.goLeft)
        base.accept('arrow_left-up', self.stop)
        base.accept('arrow_right', self.goRight)
        base.accept('arrow_right-up', self.stop)
        base.accept('arrow_up', self.goUp)
        base.accept('arrow_up-up', self.stop)
        base.accept('arrow_down', self.goDown)
        base.accept('arrow_down-up', self.stop)


    def accelerate(self):
        self.accelerating = True

    def accelerateStop(self):
        self.accelerating = False

    def goLeft(self):
        self.direction = (-1, 0)

    def goRight(self):
        self.direction = (1, 0)

    def goUp(self):
        self.direction = (0, 1)

    def goDown(self):
        self.direction = (0, -1)

    def stop(self):
        self.direction = (0, 0)