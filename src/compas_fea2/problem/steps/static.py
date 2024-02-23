from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Iterable

from compas_fea2.model.nodes import Node
from compas_fea2.problem.loads import GravityLoad
from compas_fea2.problem.loads import NodeLoad
from compas_fea2.problem.patterns import (
    Pattern,
    PointLoadPattern,
    NodeLoadPattern,
    LineLoadPattern,
    AreaLoadPattern,
    VolumeLoadPattern
    )

from compas_fea2.problem.displacements import GeneralDisplacement
from compas_fea2.problem.fields import PrescribedTemperatureField

from .step import GeneralStep


class StaticStep(GeneralStep):
    """StaticStep for use in a static analysis.

    Parameters
    ----------
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.
    loads : dict
        Dictionary of the loads assigned to each part in the model in the step.
    gravity : :class:`compas_fea2.problem.GravityLoad`
        Gravity load to assing to the whole model.
    displacements : dict
        Dictionary of the displacements assigned to each part in the model in the step.

    """

    def __init__(
        self,
        max_increments=100,
        initial_inc_size=1,
        min_inc_size=0.00001,
        time=1,
        nlgeom=False,
        modify=True,
        name=None,
        **kwargs,
    ):
        super(StaticStep, self).__init__(
            max_increments=max_increments,
            initial_inc_size=initial_inc_size,
            min_inc_size=min_inc_size,
            time=time,
            nlgeom=nlgeom,
            modify=modify,
            name=name,
            **kwargs,
        )

    def add_node_pattern(self, nodes, load_case=None,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        axes="global", name=None,
        **kwargs
    ):
        """Add a :class:`compas_fea2.problem.PointLoad` subclass object to the
        ``Step`` at specific points.

        Parameters
        ----------
        name : str
            name of the point load
        x : float, optional
            x component (in global coordinates) of the point load, by default None
        y : float, optional
            y component (in global coordinates) of the point load, by default None
        z : float, optional
            z component (in global coordinates) of the point load, by default None
        xx : float, optional
            moment about the global x axis of the point load, by default None
        yy : float, optional
            moment about the global y axis of the point load, by default None
        zz : float, optional
            moment about the global z axis of the point load, by default None
        axes : str, optional
            'local' or 'global' axes, by default 'global'

        Returns
        -------
        :class:`compas_fea2.problem.PointLoad`

        Warnings
        --------
        local axes are not supported yet

        """
        return self.add_load_pattern(NodeLoadPattern(nodes=nodes,
                            x=x, y=y, z=z, xx=xx, yy=yy, zz=zz,
                            load_case=load_case, name=name, axes=axes, **kwargs))

    def add_point_pattern(self, points, load_case=None,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        axes="global", name=None, tolerance=None,
        **kwargs
    ):
        """Add a :class:`compas_fea2.problem.PointLoad` subclass object to the
        ``Step`` at specific points.

        Parameters
        ----------
        name : str
            name of the point load
        x : float, optional
            x component (in global coordinates) of the point load, by default None
        y : float, optional
            y component (in global coordinates) of the point load, by default None
        z : float, optional
            z component (in global coordinates) of the point load, by default None
        xx : float, optional
            moment about the global x axis of the point load, by default None
        yy : float, optional
            moment about the global y axis of the point load, by default None
        zz : float, optional
            moment about the global z axis of the point load, by default None
        axes : str, optional
            'local' or 'global' axes, by default 'global'

        Returns
        -------
        :class:`compas_fea2.problem.PointLoad`

        Warnings
        --------
        local axes are not supported yet

        """
        return self.add_load_pattern(PointLoadPattern(points=points,
                            x=x, y=y, z=z, xx=xx, yy=yy, zz=zz,
                            load_case=load_case, name=name, axes=axes, tolerance=tolerance, **kwargs))


    def add_prestress_load(self):
        raise NotImplementedError

    def add_line_load(self, polyline, load_case=None, discretization=10,
        x=None, y=None, z=None, xx=None, yy=None, zz=None,
        axes="global", name=None, tolerance=None,
        **kwargs
    ):
        """Add a :class:`compas_fea2.problem.PointLoad` subclass object to the
        ``Step`` along a prescribed path.

        Parameters
        ----------
        name : str
            name of the point load
        part : str
            name of the :class:`compas_fea2.problem.DeformablePart` where the load is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a NodesGroup of the nodes where the load is
            applied.
        x : float, optional
            x component (in global coordinates) of the point load, by default None
        y : float, optional
            y component (in global coordinates) of the point load, by default None
        z : float, optional
            z component (in global coordinates) of the point load, by default None
        xx : float, optional
            moment about the global x axis of the point load, by default None
        yy : float, optional
            moment about the global y axis of the point load, by default None
        zz : float, optional
            moment about the global z axis of the point load, by default None
        axes : str, optional
            'local' or 'global' axes, by default 'global'

        Returns
        -------
        :class:`compas_fea2.problem.PointLoad`

        Warnings
        --------
        local axes are not supported yet

        """
        return self.add_load_pattern(LineLoadPattern(polyline=polyline,
                            x=x, y=y, z=z, xx=xx, yy=yy, zz=zz,
                            load_case=load_case, name=name, axes=axes,
                            tolerance=tolerance, discretization=discretization, **kwargs))

    def add_area_pattern(
        self, polygon, load_case=None, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", name=None, **kwargs
    ):
        """Add a :class:`compas_fea2.problem.PointLoad` subclass object to the
        ``Step`` along a prescribed path.

        Parameters
        ----------
        name : str
            name of the point load
        part : str
            name of the :class:`compas_fea2.problem.DeformablePart` where the load is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a NodesGroup of the nodes where the load is
            applied.
        x : float, optional
            x component (in global coordinates) of the point load, by default None
        y : float, optional
            y component (in global coordinates) of the point load, by default None
        z : float, optional
            z component (in global coordinates) of the point load, by default None
        xx : float, optional
            moment about the global x axis of the point load, by default None
        yy : float, optional
            moment about the global y axis of the point load, by default None
        zz : float, optional
            moment about the global z axis of the point load, by default None
        axes : str, optional
            'local' or 'global' axes, by default 'global'

        Returns
        -------
        :class:`compas_fea2.problem.PointLoad`

        Warnings
        --------
        local axes are not supported yet

        """
        return self.add_load_pattern(AreaLoadPattern(polygon=polygon,
                           x=x, y=y, z=z, xx=xx, yy=yy, zz=zz,
                           load_case=load_case, axes=axes, name=name, **kwargs))


    def add_tributary_load(self):
        raise NotImplementedError

    def add_gravity_load_pattern(self, parts, g=9.81, x=0.0, y=0.0, z=-1.0, name=None, load_case=None, **kwargs):
        """Add a :class:`compas_fea2.problem.GravityLoad` load to the ``Step``

        Parameters
        ----------
        g : float, optional
            acceleration of gravity, by default 9.81
        x : float, optional
            x component of the gravity direction vector (in global coordinates), by default 0.
        y : [type], optional
            y component of the gravity direction vector (in global coordinates), by default 0.
        z : [type], optional
            z component of the gravity direction vector (in global coordinates), by default -1.
        distribution : [:class:`compas_fea2.model.PartsGroup`] | [:class:`compas_fea2.model.ElementsGroup`]
            Group of parts or elements affected by gravity.

        Notes
        -----
        The gravity field is applied to the whole model. To remove parts of the
        model from the calculation of the gravity force, you can assign to them
        a 0 mass material.

        Warnings
        --------
        Be careful to assign a value of *g* consistent with the units in your
        model!

        """
        return self.add_load_pattern(VolumeLoadPattern(parts=parts, x=g*x, y=g*y, z=g*z, name=name, load_case=load_case, **kwargs))

    # =========================================================================
    #                           Fields methods
    # =========================================================================
    # FIXME change to pattern
    def add_temperature_field(self, field, node):
        raise NotImplementedError()
        # if not isinstance(field, PrescribedTemperatureField):
        #     raise TypeError("{!r} is not a PrescribedTemperatureField.".format(field))

        # if not isinstance(node, Node):
        #     raise TypeError("{!r} is not a Node.".format(node))

        # node._temperature = field
        # self._fields.setdefault(node.part, {}).setdefault(field, set()).add(node)
        # return field

    def add_temperature_fields(self, field, nodes):
        raise NotImplementedError()
        # return [self.add_temperature_field(field, node) for node in nodes]

    # =========================================================================
    #                           Displacements methods
    # =========================================================================
    def add_displacement(
        self, nodes, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", name=None, **kwargs
    ):
        """Add a displacement at give nodes to the Step object.

        Parameters
        ----------
        displacement : obj
            :class:`compas_fea2.problem.GeneralDisplacement` object.

        Returns
        -------
        None

        """
        raise NotImplementedError()
        # if axes != "global":
        #     raise NotImplementedError("local axes are not supported yet")
        # displacement = GeneralDisplacement(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
        # if not isinstance(nodes, Iterable):
        #     nodes = [nodes]
        # return self.add_load_pattern(Pattern(value=displacement, distribution=nodes))


class StaticRiksStep(StaticStep):
    """Step for use in a static analysis when Riks method is necessary."""

    def __init__(
        self,
        max_increments=100,
        initial_inc_size=1,
        min_inc_size=0.00001,
        time=1,
        nlgeom=False,
        modify=True,
        name=None,
        **kwargs,
    ):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        raise NotImplementedError
