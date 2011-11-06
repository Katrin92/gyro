from pandac.PandaModules import OdeBody, OdeMass, OdeBoxGeom, Vec3

class Obstacle:

    def __init__(self, x, y, z):

        self.model = loader.loadModel("cube")
        self.model.reparentTo(render)
        self.model.setPos(x, y, z)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(0.9, 0.9, 0.9, 1)
        self.model.setTexture(loader.loadTexture('texture.png'))

    def enable_physics(self, physics):

        self.body = OdeBody(physics.world)
        self.initial_position = self.model.getPos(render)
        self.initial_quaternion = self.model.getQuat(render)
        self.reset()

        mass = OdeMass()
        mass.setBox(0.2, 1, 1, 1)
        self.body.setMass(mass)

        self.geom = OdeBoxGeom(physics.space, 1, 1, 1)
        self.geom.setBody(self.body)

        physics.bodymodels[self.body] = self.model

    def reset(self):
        self.body.setPosition(self.initial_position)
        self.body.setQuaternion(self.initial_quaternion)
        self.body.setLinearVel(0, 0, 0)
        self.body.setAngularVel(0, 0, 0)
