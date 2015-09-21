import physical_object

class Obstacle(physical_object.Physical_Object):
    def __init__(self, polygon_list):
        self.polygon_list = polygon_list
        super().__init__()

