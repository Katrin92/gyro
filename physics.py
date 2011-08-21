from pandac.PandaModules import OdeWorld, OdeSimpleSpace, OdeJointGroup, Quat

class Physics:

    def __init__(self):
        self._init_world()
        self._init_collision()
        self._init_simulation()

    def _init_world(self):
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 1.0, 0.5, 0.0, 0.9, 0.00001, 0.0, 0.002)

    def _init_collision(self):
        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)

    def _init_simulation(self):
        self.bodymodels = {}
        self.actions = []
        self.stepSize = 1.0 / 1000.0
        self.deltaTimeAccumulator = 0
        taskMgr.doMethodLater(1.0, self._simulation_task, "Physics")

    def _simulation_task(self, task):
        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize:
            self.deltaTimeAccumulator -= self.stepSize
            for action in self.actions:
                action()
            self.space.autoCollide()
            self.world.quickStep(self.stepSize)
            for body in self.bodymodels:
                self.bodymodels[body].setPosQuat(render, body.getPosition(),
                                                 Quat(body.getQuaternion()))
            self.contactgroup.empty()
        return task.cont