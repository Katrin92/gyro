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
        self.body.setPosition(self.model.getPos(render))
        self.body.setQuaternion(self.model.getQuat(render))

        mass = OdeMass()
        mass.setBox(1, 1, 1, 0.2)
        self.body.setMass(mass)

        self.geom = OdeBoxGeom(physics.space, 1, 1, 1)
        self.geom.setBody(self.body)

        physics.bodymodels[self.body] = self.model
