from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
from typing import Iterable

from compas_fea2.base import FEAData
from compas_fea2.problem.loads import ConcentratedLoad, GravityLoad

# TODO implement __*__ magic method for combination


class Pattern(FEAData):
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
    load_case : object, optional
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
        load,
        distribution,
        load_case=None,
        **kwargs,
    ):
        super(Pattern, self).__init__(**kwargs)
        self._load = load
        self._distribution = distribution if isinstance(distribution, Iterable) else [distribution]
        self._nodes = None
        self.load_case = load_case
        self._registration = None
        
    @property
    def load(self):
        return self._load
    
    @property
    def distribution(self):
        return self._distribution

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step._registration

    @property
    def model(self):
        return self.problem._registration

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


class NodeLoadPattern(Pattern):
    """Nodal distribution of a load case.

    Parameters
    ----------
    load : object
        The load to be applied.
    nodes : list
        List of nodes where the load is applied.
    load_case : object, optional
        The load case to which this pattern belongs.
    """

    def __init__(self, load, nodes, load_case=None, **kwargs):
        super(NodeLoadPattern, self).__init__(load=load, distribution=nodes, load_case=load_case, **kwargs)

    @property
    def nodes(self):
        return self._distribution
    
    @property
    def load(self):
        return self._load

    @property
    def node_load(self):
        return zip(self.nodes, [self.load]*len(self.nodes))


class PointLoadPattern(NodeLoadPattern):
    """Point distribution of a load case.

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

    def __init__(self, load, points, load_case=None, tolerance=1, **kwargs):
        super(PointLoadPattern, self).__init__(load, points, load_case, **kwargs)
        self.tolerance = tolerance

    @property
    def points(self):
        return self._distribution

    @property
    def nodes(self):
        return [self.model.find_closest_nodes_to_point(point, distance=self.tolerance)[0] for point in self.points]


class LineLoadPattern(Pattern):
    """Line distribution of a load case.

    Parameters
    ----------
    load : object
        The load to be applied.
    polyline : object
        The polyline along which the load is distributed.
    load_case : object, optional
        The load case to which this pattern belongs.
    tolerance : float, optional
        Tolerance for finding the closest nodes to the polyline.
    discretization : int, optional
        Number of segments to divide the polyline into.
    """

    def __init__(self, load, polyline, load_case=None, tolerance=1, discretization=10, **kwargs):
        if not isinstance(load, ConcentratedLoad):
            raise TypeError("LineLoadPattern only supports ConcentratedLoad")
        super(LineLoadPattern, self).__init__(load, polyline, load_case, **kwargs)
        self.tolerance = tolerance
        self.discretization = discretization

    @property
    def polyline(self):
        return self._distribution
    
    @property
    def points(self):
        return self.polyline.divide_polyline(self.discretization)

    @property
    def nodes(self):
        return [self.model.find_closest_nodes_to_point(point, distance=self.distance)[0] for point in self.points]

    @property
    def node_load(self):
        return zip(self.nodes, [self.load] * self.nodes)


class AreaLoadPattern(Pattern):
    """Area distribution of a load case.

    Parameters
    ----------
    load : object
        The load to be applied.
    polygon : object
        The polygon defining the area where the load is distributed.
    load_case : object, optional
        The load case to which this pattern belongs.
    tolerance : float, optional
        Tolerance for finding the nodes within the polygon.
    """

    def __init__(self, load, polygon, load_case=None, tolerance=1.05, **kwargs):
        if not isinstance(load, ConcentratedLoad):
            raise TypeError("For the moment AreaLoadPattern only supports ConcentratedLoad")
        super(AreaLoadPattern, self).__init__(load=load, distribution=polygon, load_case=load_case, **kwargs)
        self.tolerance = tolerance

    @property
    def polygon(self):
        return self._distribution

    @property
    def nodes(self):
        return self.model.find_nodes_in_polygon(self.polygon, tolerance=self.tolerance)

    @property
    def node_load(self):
        return zip(self.nodes, [self.load] * self.nodes)

class VolumeLoadPattern(Pattern):
    """Volume distribution of a load case (e.g., gravity load).

    Parameters
    ----------
    load : object
        The load to be applied.
    parts : list
        List of parts where the load is applied.
    load_case : object, optional
        The load case to which this pattern belongs.
    """

    def __init__(self, load, parts,  load_case=None,  **kwargs):
        if not isinstance(load, GravityLoad):
            raise TypeError("For the moment VolumeLoadPattern only supports ConcentratedLoad")
        super(VolumeLoadPattern, self).__init__(load, parts, load_case, **kwargs)

    @property
    def parts(self):
        return self._distribution

    @property
    def nodes(self):
        return list(set(itertools.chain.from_iterable(self.parts)))

    @property
    def node_load(self):
        nodes_loads = {}
        for part in self.parts:
            for element in part.elements:
                vol = element.volume
                den = element.section.material.density
                n_nodes = len(element.nodes)
                load = ConcentratedLoad(**{k: v * vol * den / n_nodes if v else v for k, v in self.load.components.items()})
                for node in element.nodes:
                    if node in nodes_loads:
                        nodes_loads[node] += load
                    else:
                        nodes_loads[node] = load
        return zip(list(nodes_loads.keys()), list(nodes_loads.values()))
