from panda3d.core import VBase3
from pandac.PandaModules import OdeBody, OdeMass
from pandac.PandaModules import OdeTriMeshData, OdeTriMeshGeom

class Player:

    def __init__(self):
        self._init_model()

    def _init_model(self):
        self.model = loader.loadModel("test")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 2)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(0.1, 0.7, 0.7, 1)
        self.model.setTexture(loader.loadTexture('maps/noise.rgb'))

    def enable_physics(self, physics):
        self.body = OdeBody(physics.world)
        self.body.setPosition(self.model.getPos(render))
        self.body.setQuaternion(self.model.getQuat(render))
        self.body.setAngularVel(0, 0, 30)

        mass = OdeMass()
        mass.setCylinder(10, 2, 1.2, 0.2)
        self.body.setMass(mass)

        modelTrimesh = OdeTriMeshData(loader.loadModel("test"), True)
        modelGeom = OdeTriMeshGeom(physics.space, modelTrimesh)
        modelGeom.setBody(self.body)

        physics.bodymodels[self.body] = self.model
