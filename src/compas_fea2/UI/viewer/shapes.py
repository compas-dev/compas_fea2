from compas.geometry import Cone
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Box


class BCShape():
    def __init__(self, xyz, direction, scale):
        self.x, self.y, self.z = xyz
        self.direction = direction
        self.scale = scale


class PinBCShape(BCShape):
    def __init__(self, xyz, direction=[0, 0, 1], scale=1):
        super(PinBCShape, self).__init__(xyz, direction, scale)
        self.height = 0.4*self.scale
        self.diameter = 0.4*self.scale
        # FIXME this is wrong because it should follow the normal
        self.plane = Plane([self.x, self.y, self.z-self.height], direction)
        self.circle = Circle(self.plane, self.diameter)
        self.shape = Cone(self.circle, self.height)


class FixBCShape(BCShape):
    def __init__(self, xyz, scale=1):
        super(FixBCShape, self).__init__(xyz, [0, 0, 1], scale)
        self.height = 0.8*self.scale
        self.shape = Box(([self.x, self.y, self.z-self.height/4], [1, 0, 0],
                          [0, 1, 0]), self.height, self.height, self.height/2)


class MomentShape(BCShape):
    pass
