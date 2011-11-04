from plate import Plate

class Level:

    def __init__(self):      
        self._init_mouse()

    def _init_mouse(self):
        taskMgr.add(self._mouse_task, "MouseTask")
        self.reset()
        
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
        for level_object in self.objects:
            level_object.enable_physics(physics)
            
    def reset(self):
        self.smooth_x = 0
        self.smooth_y = 0
        self.mouse_x = 0
        self.mouse_y = 0  
