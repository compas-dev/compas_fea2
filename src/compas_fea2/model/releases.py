from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class BeamEndRelease(FEAData):
    """Assign an end release to a `compas_fea2.model.BeamElement`.

    Parameters
    ----------
    name : str
        Name of the BeamEndRelease object.
    location : str
        'start' or 'end'
    x : bool, optional
        Release displacements along global x direction, by default False
    y : bool, optional
        Release displacements along global y direction, by default False
    z : bool, optional
        Release displacements along global z direction, by default False
    xx : bool, optional
        Release rotations about global x direction, by default False
    yy : bool, optional
        Release rotations about global y direction, by default False
    zz : bool, optional
        Release rotations about global z direction, by default False
    """

    def __init__(self, element, location, x=False, y=False, z=False, xx=False, yy=False, zz=False):
        self.element = element
        self.location = location
        self.x = 0
        self.y = 0
        self.z = 0
        self.xx = 0
        self.yy = 0
        self.zz = 0
