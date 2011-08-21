from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import AntialiasAttrib, Spotlight, AmbientLight 
from panda3d.core import VBase3, VBase4, CardMaker
from pandac.PandaModules import OdeWorld, OdeBody, OdeMass, OdeSimpleSpace
from pandac.PandaModules import Quat, Vec4, OdeTriMeshData, OdeJointGroup
from pandac.PandaModules import OdePlaneGeom, OdeTriMeshGeom, OdeSphereGeom
from pandac.PandaModules import BitMask32

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
        self.disableMouse()
        self.setFrameRateMeter(True)
        
        self.camLens.setNearFar(1, 100)
        
        render.setShaderAuto()
        render.setAntialias(AntialiasAttrib.MAuto)
 
        self.gyro = self.loader.loadModel("gyro")
        self.gyro.reparentTo(self.render)
        self.gyro.setPos(0, 0, 2)
        self.gyro.setHpr(0, 0, 0)
        self.gyro.setColor(0.1, 0.7, 0.7, 1)
        
        tex = loader.loadTexture('maps/noise.rgb')
        self.gyro.setTexture(tex)
        
        cmaker = CardMaker("ground")     
        cmaker.setFrame(-10, 10, -10, 10)       
        self.ground = render.attachNewNode(cmaker.generate())
        self.ground.setPos(0, 0, 0)
        self.ground.setHpr(0, -90, 0)
        self.ground.setTexture(tex)
               
        self.spotlight = render.attachNewNode(Spotlight('light'))
        self.spotlight.node().setScene(render)
        self.spotlight.node().setColor(VBase4(0.8, 0.8, 0.8, 1))        
        self.spotlight.node().setShadowCaster(True, 1024, 1024)
        self.spotlight.node().getLens().setNearFar(5, 20)
        self.spotlight.node().getLens().setFov(40)
        render.setLight(self.spotlight)
        
        alight = render.attachNewNode(AmbientLight('alight'))
        alight.node().setColor(VBase4(0.1, 0.1, 0.1, 1))
        render.setLight(alight)
        
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 1.0, 0.5, 0.0, 0.9, 0.00001, 0.0, 0.002)
        
        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
                
        self.groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))
                
        self.body = OdeBody(self.world)
        self.body.setPosition(self.gyro.getPos(render))
        self.body.setQuaternion(self.gyro.getQuat(render))
        self.body.setAngularVel(0, 0, 0)
        self.mass = OdeMass()
        self.mass.setCylinder(10, 2, 1.0, 0.5)
        self.body.setMass(self.mass)        
        
        modelTrimesh = OdeTriMeshData(self.loader.loadModel("gyro-low"), True)
        modelGeom = OdeTriMeshGeom(self.space, modelTrimesh)
        modelGeom.setBody(self.body)
        
        self.deltaTimeAccumulator = 0.0
        self.stepSize = 1.0 / 1000.0
        
        self.taskMgr.add(self.cameraTask, "CameraTask")
        self.taskMgr.add(self.lightTask, "LightTask")
        self.taskMgr.doMethodLater(1.0, self.simulationTask, "Physics")
  
        self.accept('space', self.accelerate)
        self.accept('space-up', self.accelerateStop)
        self.accelerateStop()
        
        self.accept('arrow_left', self.goLeft)
        self.accept('arrow_left-up', self.stop)
        self.accept('arrow_right', self.goRight)
        self.accept('arrow_right-up', self.stop)
        self.accept('arrow_up', self.goUp)
        self.accept('arrow_up-up', self.stop)
        self.accept('arrow_down', self.goDown)
        self.accept('arrow_down-up', self.stop)
        self.stop()
  
    def cameraTask(self, task):       
        self.camera.setPos(0, -10, 15)
        self.camera.lookAt(self.gyro)        
        return Task.cont
        
    def lightTask(self, task):       
        self.spotlight.setPos(5, -5, 5)
        self.spotlight.lookAt(self.gyro)
        return Task.cont      
        
    def simulationTask(self, task):        
        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize:
            self.deltaTimeAccumulator -= self.stepSize
            avel = self.body.getAngularVel()
            if self.accelerating and avel.z < 30:
                self.body.addRelTorque(0, 0, 50)
            x, y = self.direction
            self.body.addForceAtRelPos(x*10*(abs(avel.z)+5), 
                                       y*10*(abs(avel.z)+5), 
                                       0, 0, 0, -0.3)
            rot = self.body.getRotation()            
            corr = rot.xformVec(VBase3(0, 0, 1))
            self.body.addTorque((corr.y*-50 - avel.x*50)*abs(avel.z), 
                                (corr.x* 50 - avel.y*50)*abs(avel.z), 0)
            self.space.autoCollide()
            self.world.quickStep(self.stepSize)
            self.gyro.setPosQuat(render, self.body.getPosition(), 
                                 Quat(self.body.getQuaternion()))
            self.contactgroup.empty()
        return task.cont
        
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
   
 
app = MyApp()
app.run()
