from panda3d.core import VBase3, Mat3
from pandac.PandaModules import OdeBody, OdeMass, OdeUtil
from pandac.PandaModules import OdeTriMeshData, OdeTriMeshGeom

import math

from plate import Plate

class Player:

    def __init__(self, level):
        self._init_model()
        self._init_controls()
        self.level = level

    def _init_model(self):
        self.model = loader.loadModel("test")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 2)
        self.model.setHpr(0, 0, 0)
        self.model.setColor(0.1, 0.7, 0.7, 1)
        self.model.setTexture(loader.loadTexture('texture.png'))

    def _init_controls(self):
        self.controls = Controls()

    def enable_physics(self, physics):
        self.body = OdeBody(physics.world)
        self.initial_position = self.model.getPos(render)
        self.initial_quaternion = self.model.getQuat(render)
        self.reset()

        mass = OdeMass()
        mass.setCylinder(10, 2, 1.2, 0.2)
        self.body.setMass(mass)

        modelTrimesh = OdeTriMeshData(loader.loadModel("test"), True)
        self.geom = OdeTriMeshGeom(physics.space, modelTrimesh)
        self.geom.setBody(self.body)

        physics.bodymodels[self.body] = self.model

        physics.actions.append(self._player_controls)


    def _player_controls(self):

        on_plate = False


        for level_object in self.level.objects:
            collide = OdeUtil.collide(level_object.geom, self.geom)
            if collide:
                on_plate = True
                break

        avel = self.body.getAngularVel()

        self.f = max(self.f, (1/(abs(avel.z/500)+1)))

        f = self.f
        print "Energy:", max(0, round((0.99-f)*1000,1))

        if f > 0.99:
            return

        if on_plate:
            self.body.addForce(self.controls.direction[1]*350,
                               -self.controls.direction[0]*350,
                               0)

            if self.controls.jump:
                vel = self.body.getLinearVel()
                self.body.setLinearVel(vel.x, vel.y, vel.z + 5)
                self.controls.jump = False

        hpr = self.model.getHpr()
        self.model.setHpr(hpr.x, f*hpr.y, f*hpr.z)
        self.body.setQuaternion(self.model.getQuat(render))

        self.body.setAngularVel(f*avel.x, f*avel.y, avel.z)


    def reset(self):
        self.body.setPosition(self.initial_position)
        self.body.setQuaternion(self.initial_quaternion)
        self.body.setLinearVel(0, 0, 0)
        self.body.setAngularVel(0, 0, 50)
        self.f = 0


class Controls:

    def __init__(self):
        self.stop()

        base.accept('a', self.goLeft)
        base.accept('a-up', self.stop)
        base.accept('d', self.goRight)
        base.accept('d-up', self.stop)
        base.accept('w', self.goUp)
        base.accept('w-up', self.stop)
        base.accept('s', self.goDown)
        base.accept('s-up', self.stop)

        base.accept('space', self.jump)
        self.jump = False

        base.accept('collision', self._handle_collision)

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

    def jump(self):
        self.jump = True

    def _handle_collision(self, entry):
        pass
