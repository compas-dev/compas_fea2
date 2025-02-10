from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Transformation
from compas.geometry import centroid_points_weighted
from compas.geometry import dot_vectors
from compas.geometry import transform_points
from compas.itertools import pairwise
from compas.geometry import bestfit_frame_numpy


class Interface(FEAData):
    """
    A data structure for representing interfaces between blocks
    and managing their geometrical and structural properties.

    Parameters
    ----------
    size
    points
    frame
    forces
    mesh

    Attributes
    ----------
    points : list[:class:`Point`]
        The corner points of the interface polygon.
    size : float
        The area of the interface polygon.
    frame : :class:`Frame`
        The local coordinate frame of the interface polygon.
    polygon : :class:`Polygon`
        The polygon defining the contact interface.
    mesh : :class:`Mesh`
        A mesh representation of the interface.
    kern : :class:`Polygon`
        The "kern" part of the interface polygon.
    forces : list[dict]
        A dictionary of force components per interface point.
        Each dictionary contains the following items: ``{"c_np": ..., "c_nn": ...,  "c_u": ..., "c_v": ...}``.
    stressdistribution : ???
        ???
    normalforces : list[:class:`Line`]
        A list of lines representing the normal components of the contact forces at the corners of the interface.
        The length of each line is proportional to the magnitude of the corresponding force.
    compressionforces : list[:class:`Line`]
        A list of lines representing the compression components of the normal contact forces
        at the corners of the interface.
        The length of each line is proportional to the magnitude of the corresponding force.
    tensionforces : list[:class:`Line`]
        A list of lines representing the tension components of the normal contact forces
        at the corners of the interface.
        The length of each line is proportional to the magnitude of the corresponding force.
    frictionforces : list[:class:`Line`]
        A list of lines representing the friction or tangential components of the contact forces
        at the corners of the interface.
        The length of each line is proportional to the magnitude of the corresponding force.
    resultantforce : list[:class:`Line`]
        A list with a single line representing the resultant of all the contact forces at the corners of the interface.
        The length of the line is proportional to the magnitude of the resultant force.
    resultantpoint : :class:`Point`
        The point of application of the resultant force on the interface.

    """

    @property
    def __data__(self):
        return {
            "points": self.boundary_points,
            "size": self.size,
            "frame": self.frame,
            "forces": self.forces,
            "mesh": self.mesh,
        }

    @classmethod
    def __from_data__(cls, data):
        """Construct an interface from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas_assembly.datastructures.Interface`

        """
        return cls(**data)

    def __init__(
        self,
        mesh: Mesh = None,
    ):
        super(Interface, self).__init__()
        self._mesh = mesh
        self._frame = None

    @property
    def mesh(self) -> Mesh:
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    @property
    def average_plane(self):
        pass

    @property
    def points(self):
        return [Point(*self.mesh.vertex_coordinates(v)) for v in self.mesh.vertices()]

    @property
    def boundary_points(self):
        return [Point(*self.mesh.vertex_coordinates(v)) for v in self.mesh.vertices_on_boundary()]

    @property
    def polygon(self):
        return Polygon(self.boundary_points)

    @property
    def area(self):
        return self.mesh.area()

    @property
    def frame(self):
        if self._frame is None:
            self._frame = Frame(*bestfit_frame_numpy(self.boundary_points))
        return self._frame
