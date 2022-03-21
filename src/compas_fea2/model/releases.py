from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas.geometry import Frame


class BeamEndRelease(FEAData):
    """Assign a general end release to a `compas_fea2.model.BeamElement`.

    Parameters
    ----------
    name : str
        Name of the BeamEndRelease object.
    location : str
        'start' or 'end'
    local : bool
        If True, use the local axes as reference frame for the release, by default False.
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

    def __init__(self, element, location, local=False, x=False, y=False, z=False, xx=False, yy=False, zz=False):
        self.element = element
        self.location = location
        self.local = local
        self.x = x
        self.y = y
        self.z = z
        self.xx = xx
        self.yy = yy
        self.zz = zz


class BeamEndPinRelease(BeamEndRelease):
    pass


class BeamEndSliderRelease(BeamEndRelease):
    pass
