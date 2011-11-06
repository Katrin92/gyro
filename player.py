from panda3d.core import VBase3, Mat3
from pandac.PandaModules import OdeBody, OdeMass, OdeUtil
from pandac.PandaModules import OdeTriMeshData, OdeTriMeshGeom

import math

from accelerator import Accelerator

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
        self.model.setTexture(loader.loadTexture('textures/texture.png'))

    def _init_controls(self):
        self.controls = Controls()

    def enable_physics(self, physics):
        self.body = OdeBody(physics.world)
        self.initial_position = self.model.getPos(render)
        self.initial_quaternion = self.model.getQuat(render)
        self.initial_spin_velocity = 50
        self.reset()

        mass = OdeMass()
        mass.setCylinder(10, 2, 1.2, 0.2)
        self.body.setMass(mass)

        modelTrimesh = OdeTriMeshData(loader.loadModel("test"), True)
        self.geom = OdeTriMeshGeom(physics.space, modelTrimesh)
        self.geom.setBody(self.body)

        physics.bodymodels[self.body] = self.model

        physics.actions.append(self._player_controls)
        self.exponent = 1000 * physics.step_size


    def _player_controls(self):

        avel = self.body.getAngularVel()

        on_plate = False
        accelerate = False

        for level_object in self.level.objects:
            collide = OdeUtil.collide(level_object.geom, self.geom)
            if collide:
                on_plate = True
                if avel.z < self.initial_spin_velocity and \
                   isinstance(level_object, Accelerator):
                    accelerate = level_object.player_interact(self)
                break

        if accelerate:
            avel.z += self.exponent / 200.0
            self.factor = 0

        self.calculate_factor(avel.z)

        if self.factor > 0.99:
            return

        f = self.factor**self.exponent

        if on_plate:
            if self.controls.jump:
                vel = self.body.getLinearVel()
                self.body.setLinearVel(vel.x, vel.y, vel.z + 5)
            force = 350
        else:
            force = 25

        self.controls.jump = False

        self.body.addForce(Mat3.rotateMat(self.controls.view_rotation).xform(
                           (self.controls.y*force,
                            -0.8*self.controls.x*force,
                            0)))

        hpr = self.model.getHpr()
        self.model.setHpr(hpr.x, f*hpr.y, f*hpr.z)
        self.body.setQuaternion(self.model.getQuat(render))

        self.body.setAngularVel(f*avel.x,
                                f*avel.y,
                                avel.z)

    def calculate_factor(self, spin_velocity):
        self.factor = max(self.factor, (1/(abs(spin_velocity/500.0)+1)))
        self.health = max(0, round((0.99-self.factor)*1000,1))

    def reset(self):
        self.body.setPosition(self.initial_position)
        self.body.setQuaternion(self.initial_quaternion)
        self.body.setLinearVel(0, 0, 0)
        self.body.setAngularVel(0, 0, self.initial_spin_velocity)
        self.factor = 0
        self.calculate_factor(self.initial_spin_velocity)


class Controls:

    def __init__(self):

        base.accept('a', self.go_left)
        base.accept('a-up', self.go_right)
        base.accept('d', self.go_right)
        base.accept('d-up', self.go_left)
        base.accept('w', self.go_up)
        base.accept('w-up', self.go_down)
        base.accept('s', self.go_down)
        base.accept('s-up', self.go_up)
        self.x, self.y = 0, 0

        base.accept('arrow_left', self.view_left)
        base.accept('arrow_right', self.view_right)
        self.view_rotation = 0

        base.accept('space', self.jump)
        self.jump = False

    def go_left(self):
        self.x -= 1

    def go_right(self):
        self.x += 1

    def go_up(self):
        self.y += 1

    def go_down(self):
        self.y -= 1

    def view_left(self):
        self.view_rotation += 90

    def view_right(self):
        self.view_rotation -= 90

    def jump(self):
        self.jump = True
