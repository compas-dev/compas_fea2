from compas.geometry import Cone
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Box
from compas.geometry import Cylinder
from compas.geometry import Frame


class _BCShape:
    """Basic shape for reppresenting the boundary conditions.

    Parameters
    ----------
    x : float
        The x coordinate of the restrained node.
    y : float
        The y coordinate of the restrained node.
    z : float
        The z coordinate of the restrained node.
    direction : list
        The direction of the normal.
    scale : float
        The scale factor to apply when drawing.
    """
    def __init__(self, xyz, direction, scale):
        self.x, self.y, self.z = xyz
        self.direction = direction
        self.scale = scale


class PinBCShape(_BCShape):
    """Pin support shape. It is a cone with base diameter and height equal to
    400 units.
    """
    def __init__(self, xyz, direction=[0, 0, 1], scale=1):
        super(PinBCShape, self).__init__(xyz, direction, scale)
        self.height = 400 * self.scale
        self.diameter = 400 * self.scale
        # FIXME this is wrong because it should follow the normal
        self.plane = Plane([self.x, self.y, self.z-self.height], direction)
        self.circle = Circle(frame=self.plane.frame, radius=self.diameter/2)
        self.shape = Cone(radius=self.circle.radius, height=self.height, frame=self.plane.frame)


class FixBCShape(_BCShape):
    """Fix support shape. It is a box with height equal to 800 units
    400 units.
    """
    def __init__(self, xyz, scale=1):
        super(FixBCShape, self).__init__(xyz, [0, 0, 1], scale)
        self.height = 800*self.scale
        f=Frame([self.x, self.y, self.z-self.height/4], [1, 0, 0], [0, 1, 0])
        self.shape = Box(self.height, self.height, self.height/2, f)

# FIXME: orient according to the direction of the restrain
class RollerBCShape(_BCShape):
    """Roller support shape. It is a cylinder with height equal to 800 units
    400 units.
    """
    def __init__(self, xyz, direction=[1, 0, 0], scale=1):
        super(RollerBCShape, self).__init__(xyz, direction, scale)
        self.height = 800*self.scale
        p = Plane([self.x, self.y, self.z/2], [0, 1, 0])
        c = Circle(plane=p, radius=self.height/2)
        self.shape = Cylinder(circle=c, height=self.height)


class MomentShape(_BCShape):
    pass
