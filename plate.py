from pandac.PandaModules import OdeBoxGeom, Vec3

class Plate:

    def __init__(self, x, y, z, width, height):

        self.model = loader.loadModel("cube")
        self.model.reparentTo(render)
        self.model.setScale(width, height, 0.2)
        self.model.setPos(x, y, z)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(0.7, 0.3, 0.1, 1)
        self.model.setTexture(loader.loadTexture('textures/texture.png'))

        self.width = width
        self.height = height


    def enable_physics(self, physics):
        self.geom = OdeBoxGeom(physics.space, self.width, self.height, 0.2)
        self.geom.setPosition(self.model.getPos())
        self.geom.setQuaternion(self.model.getQuat())

    def reset(self):
        pass
