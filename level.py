class Level:

    def __init__(self):
        pass

    def enable_physics(self, physics):
        for level_object in self.objects:
            level_object.enable_physics(physics)

    def reset(self):
        for level_object in self.objects:
            level_object.reset()
