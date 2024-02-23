from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas.geometry import Vector
from compas_fea2.problem.loads import NodeLoad

import itertools
from typing import Iterable
# TODO implement __*__ magic method for combination


class Pattern(FEAData):
    """A pattern is the spatial distribution of a specific set of forces,
    displacements, temperatures, and other effects which act on a structure.
    Any combination of nodes and elements may be subjected to loading and
    kinematic conditions.

    Parameters
    ----------
    value : :class:`compas_fea2.problem._Load` | :class:`compas_fea2.problem.GeneralDisplacement`
        The load/displacement of the pattern
    distribution : list
        list of :class:`compas_fea2.model.Node` or :class:`compas_fea2.model._Element`
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    value : :class:`compas_fea2.problem._Load`
        The load of the pattern
    distribution : list
        list of :class:`compas_fea2.model.Node` or :class:`compas_fea2.model._Element`
    name : str
        Uniqe identifier.

    """

    def __init__(
        self,
        distribution,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        load_case=None, axes="global", name=None,
        **kwargs,
    ):
        super(Pattern, self).__init__(name, **kwargs)
        self._distribution = distribution if isinstance(distribution, Iterable) else [distribution]
        self._nodes = None
        self.x = x
        self.y = y
        self.z = z
        self.xx = xx
        self.yy = yy
        self.zz = zz
        self.load_case = load_case
        self.axes = axes
        if axes != "global":
            raise NotImplementedError("local axes are not supported yet")
        self._registration = None

    @property
    def components(self):
        return {i: getattr(self, i) for i in ["x", "y", "z", "xx", "yy", "zz"]}

    @property
    def n_nodes(self):
        return len(self.nodes)

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step._registration

    @property
    def model(self):
        return self.problem._registration


class NodeLoadPattern(Pattern):
    """Nodal distribution of a load case.

    Parameters
    ----------
    Pattern : _type_
        _description_
    """

    def __init__(self, nodes,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        load_case=None, axes="global", name=None, **kwargs):
        super(NodeLoadPattern, self).__init__(nodes, x, y, z, xx, yy, zz, load_case, axes, name, **kwargs)

    @property
    def nodes(self):
        return self._distribution

    @property
    def node_load(self):
        n_nodes = len(self.nodes)
        #FIXME change to tributary load for each node
        return zip(self.nodes, [NodeLoad(**{k: v if v else v for k, v in self.components.items()}, name=self.name, axes=self.axes)]*n_nodes)


class PointLoadPattern(NodeLoadPattern):
    """Point distribution of a load case.

    Parameters
    ----------
    Pattern : _type_
        _description_
    """

    def __init__(self, points,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        load_case=None, axes="global", name=None, tolerance=1, **kwargs):
        super(PointLoadPattern, self).__init__(points, x, y, z, xx, yy, zz,
                                               load_case, axes, name, **kwargs)
        self.tolerance=tolerance

    @property
    def points(self):
        return self._distribution

    @property
    def nodes(self):
        return [self.model.find_closest_nodes_to_point(point, distance=self.tolerance)[0]
                for point in self.points]


class LineLoadPattern(Pattern):
    """Line distribution of a load case.

    Parameters
    ----------
    Pattern : _type_
        _description_
    """
    def __init__(self, polyline,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        load_case=None, axes="global", name=None, tolerance=1, discretization=10,
        **kwargs):
        super(LineLoadPattern, self).__init__(polyline, x, y, z, xx, yy, zz,
                                              load_case, axes, name, **kwargs)
        self.tolerance=tolerance
        self.discretization = discretization

    @property
    def polyline(self):
        return self._distribution

    @property
    def nodes(self):
        return [
            self.model.find_closest_nodes_to_point(point, distance=self.distance)[0]
            for point in self.polyline.divide_polyline(self.discretization)
        ]

    @property
    def node_load(self):
        n_nodes = len(self.nodes)
        length = self.polyline.length
        #FIXME change to tributary load for each node
        return zip(self.nodes, [NodeLoad(**{k: v*length/n_nodes if v else v for k, v in self.components.items()},
                          name=self.name, axes=self.axes)]*n_nodes)


class AreaLoadPattern(Pattern):
    """Area distribution of a load case.

    Parameters
    ----------
    Pattern : _type_
        _description_
    """

    def __init__(self, polygon,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        load_case=None, axes="global", name=None, tolerance=1.05, **kwargs):
        super(AreaLoadPattern, self).__init__(distribution=polygon,
                                              x=x, y=y, z=z, xx=xx, yy=yy, zz=zz,
                                              load_case=load_case, axes=axes,
                                              name=name, **kwargs)
        self.tolerance=tolerance

    @property
    def polygon(self):
        return self._distribution

    @property
    def nodes(self):
        return self.model.find_nodes_in_polygon(self.polygon, tolerance=self.tolerance)

    @property
    def node_load(self):
        n_nodes = len(self.nodes)
        area = self.polygon.area
        return zip(self.nodes, [NodeLoad(**{k: v*area/n_nodes if v else v for k, v in self.components.items()},
                          name=self.name, axes=self.axes)]*n_nodes)


class VolumeLoadPattern(Pattern):
    """Volume distribution of a load case (e.g., gravity load).

    Parameters
    ----------
    Pattern : _type_
        _description_
    """

    def __init__(self, parts,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        load_case=None, axes="global", name=None, **kwargs):
        super(VolumeLoadPattern, self).__init__(parts, x, y, z, xx, yy, zz,
                                              load_case, axes, name, **kwargs)

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
                load = NodeLoad(**{k: v*vol*den/n_nodes if v else v for k, v in self.components.items()},
                    name=self.name, axes=self.axes)
                for node in element.nodes:
                    if node in nodes_loads:
                        nodes_loads[node] += load
                    else:
                        nodes_loads[node] = load
        return zip(list(nodes_loads.keys()), list(nodes_loads.values()))

