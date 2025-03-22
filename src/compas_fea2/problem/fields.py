import itertools
from typing import Iterable

from compas_fea2.base import FEAData
from compas_fea2.problem.loads import ConcentratedLoad
from compas_fea2.problem.loads import PressureLoad
from compas_fea2.problem.loads import GravityLoad

# TODO implement __*__ magic method for combination


class LoadField(FEAData):
    """A pattern is the spatial distribution of a specific set of forces,
    displacements, temperatures, and other effects which act on a structure.
    Any combination of nodes and elements may be subjected to loading and
    kinematic conditions.

    Parameters
    ----------
    load : :class:`compas_fea2.problem._Load` | :class:`compas_fea2.problem.GeneralDisplacement`
        The load/displacement assigned to the pattern.
    distribution : list
        List of :class:`compas_fea2.model.Node` or :class:`compas_fea2.model._Element`. The
        application in space of the load/displacement.
    load_case : str, optional
        The load case to which this pattern belongs.
    axes : str, optional
        Coordinate system for the load components. Default is "global".
    name : str, optional
        Unique identifier for the pattern.

    Attributes
    ----------
    load : :class:`compas_fea2.problem._Load`
        The load of the pattern.
    distribution : list
        List of :class:`compas_fea2.model.Node` or :class:`compas_fea2.model._Element`.
    name : str
        Unique identifier.

    Notes
    -----
    Patterns are registered to a :class:`compas_fea2.problem._Step`.
    """

    def __init__(
        self,
        loads,
        distribution,
        load_case=None,
        **kwargs,
    ):
        super(LoadField, self).__init__(**kwargs)
        self._distribution = distribution if isinstance(distribution, Iterable) else [distribution]
        self._loads = loads if isinstance(loads, Iterable) else [loads * (1 / len(self._distribution))] * len(self._distribution)
        self.load_case = load_case
        self._registration = None

    @property
    def loads(self):
        return self._loads

    @property
    def distribution(self):
        return self._distribution

    @property
    def step(self):
        if self._registration:
            return self._registration
        else:
            raise ValueError("Register the Pattern to a Step first.")

    @property
    def problem(self):
        return self.step.problem

    @property
    def model(self):
        return self.problem.model

    # def __add__(self, other):
    #     if not isinstance(other, Pattern):
    #         raise TypeError("Can only combine with another Pattern")
    #     combined_distribution = self._distribution + other._distribution
    #     combined_components = {k: (getattr(self, k) or 0) + (getattr(other, k) or 0) for k in self.components}
    #     return Pattern(
    #         combined_distribution,
    #         x=combined_components["x"],
    #         y=combined_components["y"],
    #         z=combined_components["z"],
    #         xx=combined_components["xx"],
    #         yy=combined_components["yy"],
    #         zz=combined_components["zz"],
    #         load_case=self.load_case or other.load_case,
    #         axes=self.axes,
    #         name=self.name or other.name,
    #     )


class NodeLoadField(LoadField):
    """A distribution of a set of concentrated loads over a set of nodes.

    Parameters
    ----------
    load : object
        The load to be applied.
    nodes : list
        List of nodes where the load is applied.
    load_case : object, optional
        The load case to which this pattern belongs.
    """

    def __init__(self, loads, nodes, load_case=None, **kwargs):
        super(NodeLoadField, self).__init__(loads=loads, distribution=nodes, load_case=load_case, **kwargs)

    @property
    def nodes(self):
        return self._distribution

    @property
    def loads(self):
        return self._loads

    @property
    def node_load(self):
        """Return a list of tuples with the nodes and the assigned load."""
        return zip(self.nodes, self.loads)


class PointLoadField(NodeLoadField):
    """A distribution of a set of concentrated loads over a set of points.
    The loads are applied to the closest nodes to the points.

    Parameters
    ----------
    load : object
        The load to be applied.
    points : list
        List of points where the load is applied.
    load_case : object, optional
        The load case to which this pattern belongs.
    tolerance : float, optional
        Tolerance for finding the closest nodes to the points.
    """

    def __init__(self, loads, points, load_case=None, tolerance=1, **kwargs):
        self._points = points
        self._tolerance = tolerance
        # FIXME: this is not working, the patternhas no model!
        distribution = [self.model.find_closest_nodes_to_point(point, distance=self._tolerance)[0] for point in self.points]
        super().__init__(loads, distribution, load_case, **kwargs)

    @property
    def points(self):
        return self._points

    @property
    def nodes(self):
        return self._distribution


# class LineLoadField(LoadField):
#     """A distribution of a concentrated load over a given polyline.

#     Parameters
#     ----------
#     load : object
#         The load to be applied.
#     polyline : object
#         The polyline along which the load is distributed.
#     load_case : object, optional
#         The load case to which this pattern belongs.
#     tolerance : float, optional
#         Tolerance for finding the closest nodes to the polyline.
#     discretization : int, optional
#         Number of segments to divide the polyline into.
#     """

#     def __init__(self, loads, polyline, load_case=None, tolerance=1, discretization=10, **kwargs):
#         if not isinstance(loads, ConcentratedLoad):
#             raise TypeError("LineLoadPattern only supports ConcentratedLoad")
#         super(LineLoadField, self).__init__(loads, polyline, load_case, **kwargs)
#         self.tolerance = tolerance
#         self.discretization = discretization

#     @property
#     def polyline(self):
#         return self._distribution

#     @property
#     def points(self):
#         return self.polyline.divide_polyline(self.discretization)

#     @property
#     def nodes(self):
#         return [self.model.find_closest_nodes_to_point(point, distance=self.distance)[0] for point in self.points]

#     @property
#     def node_load(self):
#         return zip(self.nodes, [self.loads] * self.nodes)


# class PressureLoadField(LoadField):
#     """A distribution of a pressure load over a region defined by a polygon.
#     The loads are distributed over the nodes within the region using their tributary area.

#     Parameters
#     ----------
#     load : object
#         The load to be applied.
#     polygon : object
#         The polygon defining the area where the load is distributed.
#     planar : bool, optional
#         If True, only the nodes in the same plane of the polygon are considered. Default is False.
#     load_case : object, optional
#         The load case to which this pattern belongs.
#     tolerance : float, optional
#         Tolerance for finding the nodes within the polygon.
#     """

#     def __init__(self, pressure, polygon, planar=False, load_case=None, tolerance=1.05, **kwargs):
#         if not isinstance(pressure, PressureLoad):
#             raise TypeError("For the moment PressureLoadField only supports PressureLoad")

#         super().__init__(loads=pressure, distribution=polygon, load_case=load_case, **kwargs)
#         self.tolerance = tolerance

#     @property
#     def polygon(self):
#         return self._distribution

#     @property
#     def nodes(self):
#         return self.model.find_nodes_in_polygon(self.polygon, tolerance=self.tolerance)

#     @property
#     def node_load(self):
#         return zip(self.nodes, [self.loads] * self.nodes)


# class VolumeLoadField(LoadField):
#     """Distribution of a load case (e.g., gravity load).

#     Parameters
#     ----------
#     load : object
#         The load to be applied.
#     parts : list
#         List of parts where the load is applied.
#     load_case : object, optional
#         The load case to which this pattern belongs.
#     """

#     def __init__(self, load, parts, load_case=None, **kwargs):
#         if not isinstance(load, GravityLoad):
#             raise TypeError("For the moment VolumeLoadPattern only supports ConcentratedLoad")
#         super(VolumeLoadField, self).__init__(load, parts, load_case, **kwargs)

#     @property
#     def parts(self):
#         return self._distribution

#     @property
#     def nodes(self):
#         return list(set(itertools.chain.from_iterable(self.parts)))

#     @property
#     def node_load(self):
#         nodes_loads = {}
#         for part in self.parts:
#             for element in part.elements:
#                 vol = element.volume
#                 den = element.section.material.density
#                 n_nodes = len(element.nodes)
#                 load = ConcentratedLoad(**{k: v * vol * den / n_nodes if v else v for k, v in self.loads.components.items()})
#                 for node in element.nodes:
#                     if node in nodes_loads:
#                         nodes_loads[node] += load
#                     else:
#                         nodes_loads[node] = load
#         return zip(list(nodes_loads.keys()), list(nodes_loads.values()))


class GravityLoadField(LoadField):
    """Volume distribution of a gravity load case.

    Parameters
    ----------
    g : float
        Value of gravitational acceleration.
    parts : list
        List of parts where the load is applied.
    load_case : object, optional
        The load case to which this pattern belongs.
    """

    def __init__(self, g=9.81, parts=None, load_case=None, **kwargs):
        super(GravityLoadField, self).__init__(GravityLoad(g=g), parts, load_case, **kwargs)


class _PrescribedField(FEAData):
    """Base class for all predefined initial conditions.

    Notes
    -----
    Fields are registered to a :class:`compas_fea2.problem.Step`.

    """

    def __init__(self, **kwargs):
        super(_PrescribedField, self).__init__(**kwargs)


class PrescribedTemperatureField(_PrescribedField):
    """Temperature field"""

    def __init__(self, temperature, **kwargs):
        super(PrescribedTemperatureField, self).__init__(**kwargs)
        self._t = temperature

    @property
    def temperature(self):
        return self._t

    @temperature.setter
    def temperature(self, value):
        self._t = value
