from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.nodes import Node

from compas_fea2.problem.loads import _Load
from compas_fea2.problem.loads import GravityLoad
from compas_fea2.problem.loads import PointLoad

from compas_fea2.problem.displacements import GeneralDisplacement

from .step import _GeneralStep


class StaticStep(_GeneralStep):
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

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(StaticStep, self).__init__(max_increments=max_increments,
                                         initial_inc_size=initial_inc_size, min_inc_size=min_inc_size,
                                         time=time, nlgeom=nlgeom, modify=modify, name=name, **kwargs)
        self._displacements = {}
        self._gravity = None

    @property
    def gravity(self):
        return self._gravity

    @property
    def displacements(self):
        return self._displacements

    def add_point_load(self, node, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        """Add a :class:`compas_fea2.problem.PointLoad` subclass object to the ``Step``.

        Warning
        -------
        local axes are not supported yet

        Parameters
        ----------
        name : str
            name of the point load
        part : str
            name of the :class:`compas_fea2.problem.Part` where the load is applied
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

        Return
        ------
        :class:`compas_fea2.problem.PointLoad`
        """
        if axes != 'global':
            raise NotImplementedError('local axes are not supported yet')
        return self.add_load(PointLoad(x, y, z, xx, yy, zz, axes), node)

    def add_gravity_load(self, g=9.81, x=0., y=0., z=-1.):
        """Add a :class:`compas_fea2.problem.GravityLoad` load to the ``Step``

        Warning
        -------
        Be careful to assign a value of *g* consistent with the units in your
        model!

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
        """
        self._gravity = GravityLoad(g, x, y, z)

    def add_prestress_load(self):
        raise NotImplementedError

    def add_line_load(self):
        raise NotImplementedError

    def add_area_load(self):
        raise NotImplementedError

    def add_tributary_load(self):
        raise NotImplementedError

    # =========================================================================
    #                       Displacement methods
    # =========================================================================

    def add_displacement(self, displacement, node):
        """Add a displacement to Step object.

        Parameters
        ----------
        displacement : obj
            ``compas_fea2`` :class:`compas_fea2.problem.GeneralDisplacement` object.
        where : int
            node or element key where the load is applied
        part : str
            name of the part where the load is applied
        Returns
        -------
        None
        """
        if not isinstance(displacement, GeneralDisplacement):
            raise TypeError('{!r} is not a General Displacement.'.format(displacement))

        if not isinstance(node, Node):
            raise TypeError('{!r} is not a Node.'.format(node))
        # self.model.contains_node(node) #TODO implement method
        node._displacements.add(displacement)
        self._displacements.setdefault(node.part, {}).setdefault(displacement, set()).add(node)
        return displacement

    def add_displacements(self, displacement, nodes):
        return [self.add_displacement(displacement, node) for node in nodes]


class StaticRiksStep(StaticStep):
    """Step for use in a static analysis when Riks method is necessary.

    Parameters
    ----------
    None

    Attributes
    ----------
    None

    """

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        raise NotImplementedError()
