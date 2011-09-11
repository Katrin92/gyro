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
        self.initial_position = self.model.getPos(render)
        self.initial_quaternion = self.model.getQuat(render)
        self.reset()

        mass = OdeMass()
        mass.setCylinder(10, 2, 1.2, 0.2)
        self.body.setMass(mass)

        modelTrimesh = OdeTriMeshData(loader.loadModel("test"), True)
        modelGeom = OdeTriMeshGeom(physics.space, modelTrimesh)
        modelGeom.setBody(self.body)

        physics.bodymodels[self.body] = self.model
        
        
    def reset(self):
        self.body.setPosition(self.initial_position)
        self.body.setQuaternion(self.initial_quaternion)
        self.body.setAngularVel(0, 0, 20)
        self.body.setLinearVel(0, 0, 3)
