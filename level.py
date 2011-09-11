from plate import Plate

class Level:

    def __init__(self):      
        self._init_plates()
        self._init_mouse()

    def _init_plates(self):
        self.plates = (Plate(self, -10, 0, -0.5,  4, 4,  1,  1),        
                       Plate(self,   0, 0, -1.5, 16, 2, .3,  1),
                       Plate(self,  10, 0, -2.5,  4, 4, .5, .5))

    def _init_mouse(self):
        taskMgr.add(self._mouse_task, "MouseTask")
        self.smooth_x = 0
        self.smooth_y = 0
        self.mouse_x = 0
        self.mouse_y = 0    
        
    def _mouse_task(self, task):
        if base.mouseWatcherNode.hasMouse():
        
            props = base.win.getProperties()
            winX = props.getXSize()
            winY = props.getYSize()            
            centerx = winX / 2
            centery = winY / 2         
               
            self.mouse_x+=base.mouseWatcherNode.getMouseX() * 10
            self.mouse_y+=base.mouseWatcherNode.getMouseY() * 10 
            
            max_angle = 30
            if self.mouse_x > max_angle: self.mouse_x = max_angle
            if self.mouse_x < -max_angle: self.mouse_x = -max_angle
            if self.mouse_y > max_angle: self.mouse_y = max_angle
            if self.mouse_y < -max_angle: self.mouse_y = -max_angle
                   
            self.smooth_x += (self.mouse_x - self.smooth_x) * globalClock.getDt() * 2  
            self.smooth_y += (self.mouse_y - self.smooth_y) * globalClock.getDt() * 2   
            
            base.win.movePointer(0, centerx, centery)
            
        return task.cont
        
    def enable_physics(self, physics):
        for plate in self.plates:
            plate.enable_physics(physics)
