from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Plane


class _BCShape:
    """Basic shape for reppresenting the boundary conditions.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the restrained node.
    direction : list of float, optional
        The direction of the normal. Default is [0, 0, 1].
    scale : float, optional
        The scale factor to apply when drawing. Default is 1.
    """

    def __init__(self, xyz, direction, scale):
        self.x, self.y, self.z = xyz
        self.direction = direction
        self.scale = scale


class _LoadShape:
    """Basic shape for reppresenting the boundary conditions.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the restrained node.
    direction : list of float, optional
        The direction of the normal. Default is [0, 0, 1].
    scale : float, optional
        The scale factor to apply when drawing. Default is 1.
    """

    def __init__(self, xyz, direction, scale):
        self.x, self.y, self.z = xyz
        self.direction = direction
        self.scale = scale


class PinBCShape(_BCShape):
    """Pin support shape. It is a cone with base diameter and height equal to
    400 units.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the restrained node.
    direction : list of float, optional
        The direction of the normal. Default is [0, 0, 1].
    scale : float, optional
        The scale factor to apply when drawing. Default is 1.
    """

    def __init__(self, xyz, direction=[0, 0, 1], scale=1):
        super(PinBCShape, self).__init__(xyz, direction, scale)
        self.height = 400 * self.scale
        self.diameter = 400 * self.scale
        # FIXME this is wrong because it should follow the normal
        self.plane = Plane([self.x, self.y, self.z - self.height], direction)
        self.circle = Circle(frame=Frame.from_plane(self.plane), radius=self.diameter / 2)
        self.shape = Cone(radius=self.circle.radius, height=self.height, frame=Frame.from_plane(self.plane))


class FixBCShape(_BCShape):
    """Fix support shape. It is a box with height equal to 800 units
    400 units.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the restrained node.
    scale : float, optional
        The scale factor to apply when drawing. Default is 1.
    """

    def __init__(self, xyz, scale=1):
        super(FixBCShape, self).__init__(xyz, [0, 0, 1], scale)
        self.height = 800 * self.scale
        f = Frame([self.x, self.y, self.z - self.height / 4], [1, 0, 0], [0, 1, 0])
        self.shape = Box(self.height, self.height, self.height / 2, f)


# FIXME: orient according to the direction of the restrain
class RollerBCShape(_BCShape):
    """Roller support shape. It is a cylinder with height equal to 800 units
    400 units.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the restrained node.
    direction : list of float, optional
        The direction of the normal. Default is [1, 0, 0].
    scale : float, optional
        The scale factor to apply when drawing. Default is 1.
    """

    def __init__(self, xyz, direction=[1, 0, 0], scale=1):
        super(RollerBCShape, self).__init__(xyz, direction, scale)
        self.height = 800 * self.scale
        p = Plane([self.x, self.y, self.z / 2], [0, 1, 0])
        c = Circle(plane=p, radius=self.height / 2)
        self.shape = Cylinder(circle=c, height=self.height)


class MomentShape(_BCShape):
    """Moment shape representation.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the point where the moment is applied.
    direction : list of float
        The direction of the moment.
    scale : float
        The scale factor to apply when drawing.
    """

    def __init__(self, xyz, direction=[0, 0, 1], scale=1):
        super(MomentShape, self).__init__(xyz, direction, scale)
        # Define the shape for the moment representation
        # This is a placeholder, you can define the actual shape as needed
        self.shape = None


class ArrowShape(_LoadShape):
    """Arrow shape representation.

    Parameters
    ----------
    xyz : list of float
        The coordinates of the base of the arrow.
    direction : list of float
        The direction in which the arrow points.
    scale : float
        The scale factor to apply when drawing. Default is 1.
    """

    def __init__(self, anchor, vector, scale=1):
        super(ArrowShape, self).__init__(anchor, vector, scale)
        self.height = vector.length * self.scale
        self.radius = vector.length * 0.1 * self.scale
        self.plane = Plane([self.x, self.y, self.z], vector)
        self.cone = Cone(radius=self.radius, height=self.height, frame=Frame.from_plane(self.plane))
        self.shape = self.cone
