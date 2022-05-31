from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# import pickle
# import os
import importlib
import itertools
from typing import Iterable

# import compas_fea2
from compas_fea2 import config
from compas_fea2.utilities._utils import timer
from compas_fea2.base import FEAData
from compas_fea2.model.interactions import _Interaction
from compas_fea2.model.parts import Part
from compas_fea2.model.nodes import Node
from compas_fea2.model.materials import _Material
from compas_fea2.model.sections import _Section
from compas_fea2.model.bcs import _BoundaryCondition
from compas_fea2.model.groups import _Group, NodesGroup, PartsGroup, ElementsGroup, FacesGroup
from compas_fea2.model.interfaces import Interface
from compas_fea2.model.constraints import _Constraint, TieConstraint
from compas_fea2.utilities.interfaces import faces_in_interface
from compas_fea2.utilities.interfaces import nodes_in_interface


class Model(FEAData):
    """Class representing an FEA model.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    description : str, optional
        Some description of the model, by default ``None``.
        This will be added to the input file and can be useful for future reference.
    author : str, optional
        The name of the author of the model, by default ``None``.
        This will be added to the input file and can be useful for future reference.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    description : str
        Some description of the model.
        This will be added to the input file and can be useful for future reference.
    author : str
        The name of the author of the model.
        This will be added to the input file and can be useful for future reference.
    parts : Set[:class:`compas_fea2.model.Part`]
        The parts of the model.
    bcs : dict
        The boundary conditions of the model.
    constraints : Set[:class:`compas_fea2.model._Constraint`]
        The constraints of the model.
    interactions : Set[:class:`compas_fea2.model._Interaction`]
        The interactions between parts of the model.
    interfaces : Set[:class:`compas_fea2.model._Interface`]
        The interface between two parts of the model.
    partgroups : Set[:class:`compas_fea2.model.PartsGroup`]
        The part groups of the model.
    facesgroups : Set[:class:`compas_fea2.model.FacesGroup`]
        The surfaces of the model.

    """

    def __init__(self, *, name=None, description=None, author=None, **kwargs):
        super(Model, self).__init__(name=name, **kwargs)
        self.description = description
        self.author = author
        self._parts = set()
        self._bcs = {}
        self._constraints = set()
        self._interactions = set()
        self._interfaces = set()
        self._partsgroups = set()

    @property
    def parts(self):
        return self._parts

    @property
    def partgroups(self):
        return self._partsgroups

    @property
    def bcs(self):
        return self._bcs

    @property
    def constraints(self):
        return self._constraints

    @property
    def interactions(self):
        return self._interactions

    @property
    def interfaces(self):
        return self._interfaces

    @property
    def facesgroups(self):
        return self._facesgroups

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def find_part_by_name(self, name):
        # type: (str) -> Part
        """Find if there is a part with a given name in the model.

        Parameters
        ----------
        name : str

        Returns
        -------
        :class:`compas_fea2.model.Part`

        """
        for part in self.parts:
            if part.name == name:
                return part

    def contains_part(self, part):
        # type: (Part) -> Part
        """Verify that the model contains a specific part.

        Parameters
        ----------
        part : :class:`compas_fea2.model.Part`

        Returns
        -------
        bool

        """
        return part in self.parts

    def add_part(self, part):
        # type: (Part) -> Part
        """Adds a Part to the Model.

        Parameters
        ----------
        part : :class:`compas_fea2.model.Part`

        Returns
        -------
        :class:`compas_fea2.model.Part`

        Raises
        ------
        TypeError
            If the part is not a part.

        """
        if not isinstance(part, Part):
            raise TypeError("{!r} is not a part.".format(part))

        if self.contains_part(part):
            if config.VERBOSE:
                print("SKIPPED: Part {!r} is already in the model.".format(part))
            return

        if self.find_part_by_name(part.name):
            raise ValueError("Duplicate name! The name '{}' is already in use.".format(part.name))

        part._model = self
        if config.VERBOSE:
            print("{!r} registered to {!r}.".format(part, self))

        self._parts.add(part)
        return part

    def add_parts(self, parts):
        # type: (list) -> list
        """Add multiple parts to the model.

        Parameters
        ----------
        parts : list[:class:`compas_fea2.model.Part`]

        Returns
        -------
        list[:class:`compas_fea2.model.Part`]

        """
        return [self.add_part(part) for part in parts]

    def get_node_from_coordinates(self, xyz, tol):
        # type: (list, float) -> dict
        """Finds (if any) the Node object in the model with the specified coordinates.
        A tollerance factor can be specified.

        Parameters
        ----------
        xyz : list
            List with the [x, y, z] coordinates of the Node.
        tol : int
            multiple to which round the coordinates.

        Returns
        -------
        dict
            Dictionary with the keys of the maching nodes for each Part.
            key =  Part name
            value = list of keys of the maching the specified coordinates.
        """
        return {part.name: part.get_node_from_coordinates(xyz, tol) for part in self.parts.values()}

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    def group_nodes_by_attribute(self, attr, value, tolerance, name=None):
        """Find all nodes with a given value for a the given attribute.

        Parameters
        ----------
        attr : str
            Attribute name.
        value : any
            Appropriate value for the given attribute.
        name : str, optional
            Name of the group. If not provided, one is automatically generated.

        Returns
        -------
        [:class:`compas_fea2.model.NodesGroup`]

        """
        return [NodesGroup(nodes=list(part.find_nodes_by_attribute(attr, value, tolerance)),
                           name=name) for part in self.parts if part.find_nodes_by_attribute(attr, value, tolerance)]

    def group_parts(self, group):
        """Add a Group object to a part in the Model. it can be either a
        :class:`FacesGroup` or an :class:`ElementsGroup`.

        Parameters
        ----------
        group : obj
            :class:`NodesGroup` or :class:`ElementsGroup` object to add.

        Returns
        -------
        None
        """
        self._partsgroups.add(group)
        return group

    # =========================================================================
    #                       Constraints methods
    # =========================================================================

    def add_constraint(self, constraint):
        # type: (_Constraint) -> _Constraint
        """Add a :class:`compas_fea2.model._Constraint` object to the Model.

        Parameters
        ----------
        constraint : :class:`compas_fea2.model._Constraint`
            Constraint object to add to the model.

        Returns
        -------
        :class:`compas_fea2.model.Constraint`
        """
        if isinstance(constraint, _Constraint):
            self._constraints.add(constraint)
        else:
            raise TypeError('{!r} is not a constraint.'.format(constraint))
        return constraint

    def add_constraints(self, constraints):
        # type: (list) -> list
        """Add multiple :class:`compas_fea2.model._Constraint` objects to the Model.

        Parameters
        ----------
        constraints : list[:class:`compas_fea2.model._Constraint`]
            list of constraints objects to add to the model.

        Returns
        -------
        list[:class:`compas_fea2.model._Constraint`]
        """
        return [self.add_constraint(constraint) for constraint in constraints]

    # =========================================================================
    #                        ContactPair methods
    # =========================================================================

    def add_interface(self, interface):
        # type: (Interface) -> Interface
        """Add a :class:`compas_fea2.model._Interface` object to the model.

        Parameters
        ----------
        interface : :class:`compas_fea2.model._Interface`
            Interface object to add to the model.

        Returns
        -------
        :class:`compas_fea2.model._Interface`
        """
        if isinstance(interface, Interface):
            self._interfaces.add(interface)
            if not interface.master.part:
                raise ValueError('The master surface is not registered to any part')
            if not interface.slave.part:
                raise ValueError('The slave surface is not registered to any part')
        else:
            raise TypeError('{!r} is not an interface.'.format(interface))
        self._interactions.add(interface.interaction)
        return interface

    def add_interfaces(self, interfaces):
        # type: (list) -> list
        """Add multiple :class:`compas_fea2.model.Interface` objects to the Model.

        Parameters
        ----------
        interfaces : list[:class:`compas_fea2.model._Interface`]
            List with interfaces to add to the model.

        Returns
        -------
        list[:class:`compas_fea2.model._Interface`]
        """
        return [self.add_interface(interface) for interface in interfaces]

    # =========================================================================
    #                           BCs methods
    # =========================================================================

    def add_bcs(self, bc, nodes, axes='global'):
        # type: (_BoundaryCondition, Node, str) -> _BoundaryCondition
        """Add a :class:`compas_fea2.model._BoundaryCondition` to the model.

        Note
        ----
        Currently global axes are used in the Boundary Conditions definition.

        Parameters
        ----------
        bc : :class:`compas_fea2.model._BoundaryCondition`
            Boundary condition object to add to the model.
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.

        Returns
        -------
        list[:class:`compas_fea2.model._BoundaryCondition`]

        """
        if isinstance(nodes, _Group):
            nodes = nodes._members

        if not isinstance(nodes, (list, tuple)):
            nodes = [nodes]

        if not isinstance(bc, _BoundaryCondition):
            raise TypeError('{!r} is not a _BoundaryCondition.'.format(bc))

        bcs = []
        for node in nodes:
            if not isinstance(node, Node):
                raise TypeError('{!r} is not a Node.'.format(node))
            if not node.part:
                raise ValueError('{!r} is not registered to any part.'.format(node))
            elif not node.part in self.parts:
                raise ValueError('{!r} belongs to a part not registered to this model.'.format(node))
            node.dof = bc
            self._bcs.setdefault(node.part, {}).setdefault(bc, set()).add(node)
            bcs.append(bc)
        return bcs

    def _add_bc_type(self, bc_type, nodes, axes='global'):
        # type: (str, Node, str) -> _BoundaryCondition
        """Add a :class:`compas_fea2.model._BoundaryCondition` by type.

        Note
        ----
        The bc_type must be one of the following:

        .. csv-table::
            :header: bc_type , BC

            fix, :class:`compas_fea2.model.bcs.FixedBC`
            clampXX, :class:`compas_fea2.model.bcs.ClampBCXX`
            clampYY, :class:`compas_fea2.model.bcs.ClampBCYY`
            clampZZ, :class:`compas_fea2.model.bcs.ClampBCZZ`
            pin, :class:`compas_fea2.model.bcs.PinnedBC`
            rollerX, :class:`compas_fea2.model.bcs.RollerBCX`
            rollerY, :class:`compas_fea2.model.bcs.RollerBCY`
            rollerZ, :class:`compas_fea2.model.bcs.RollerBCZ`
            rollerXY, :class:`compas_fea2.model.bcs.RollerBCXY`
            rollerYZ, :class:`compas_fea2.model.bcs.RollerBCYZ`
            rollerXZ, :class:`compas_fea2.model.bcs.RollerBCXZ`


        Parameters
        ----------
        name : str
            name of the boundary condition
        bc_type : str
            one of the boundary condition types specified above
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        types = {'fix': 'FixedBC', 'fixXX': 'FixedBCXX', 'fixYY': 'FixedBCYY',
                 'fixZZ': 'FixedBCZZ', 'pin': 'PinnedBC', 'rollerX': 'RollerBCX',
                 'rollerY': 'RollerBCY', 'rollerZ': 'RollerBCZ', 'rollerXY': 'RollerBCXY',
                 'rollerYZ': 'RollerBCYZ', 'rollerXZ': 'RollerBCXZ',
                 }
        m = importlib.import_module('compas_fea2.model.bcs')
        bc = getattr(m, types[bc_type])()
        return self.add_bcs(bc, nodes, axes)

    def add_fix_bc(self, nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a :class:`compas_fea2.model.FixedBC` to the nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('fix', nodes, axes)

    def add_pin_bc(self, nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a pinned boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('pin', nodes, axes)

    def add_clampXX_bc(self, nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a fixed boundary condition type free about XX to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('clampXX', nodes, axes)

    def add_clampYY_bc(self, nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a fixed boundary condition free about YY type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('clampYY', nodes, axes)

    def add_clampZZ_bc(self, nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a fixed boundary condition free about ZZ type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('clampZZ', nodes, axes)

    def add_rollerX_bc(self,  nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a roller free on X boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerX',  nodes, axes)

    def add_rollerY_bc(self,  nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a roller free on Y boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerY',  nodes, axes)

    def add_rollerZ_bc(self,  nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a roller free on Z boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerZ', nodes, axes)

    def add_rollerXY_bc(self,  nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a roller free on XY boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerXY',  nodes, axes)

    def add_rollerXZ_bc(self,  nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a roller free on XZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerXZ',  nodes, axes)

    def add_rollerYZ_bc(self,  nodes, axes='global'):
        # type: (Node, str) -> _BoundaryCondition
        """Add a roller free on YZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerYZ',  nodes, axes)

    def remove_bcs(self, bcs):
        """Removes multiple boundary conditions from the Model.

        Parameters
        ----------
        bc_names : list
            List of names of the boundary conditions to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_bcs(self):
        """Removes all the boundary conditions from the Model.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        raise NotImplementedError

    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        # type: () -> str
        """Prints a summary of the Model object.

        Parameters
        ----------
        None

        Returns
        -------
        str
            Model summary
        """
        parts_info = ['\n'.join(['{}'.format(part.name),
                                 '    # of nodes: {}'.format(len(part.nodes)),
                                 '    # of elements: {}'.format(len(part.elements))]) for part in self.parts]
        interactions_info = '\n'.join([e.name for e in self.interactions])
        constraints_info = '\n'.join([e.__repr__() for e in self.constraints])
        bc_info = '\n'.join(['{}: \n{}'.format(part.name, '\n'.join(['  {!r} - # of restrained nodes {}'.format(bc, len(nodes))
                                                                     for bc, nodes in bc_nodes.items()])) for part, bc_nodes in self.bcs.items()])
        data = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Model: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {}
author: {}

Parts
-----
{}

Interactions
------------
{}

Constraints
-----------
{}

Boundary Conditions
-------------------
{}
""".format(self.name,
           self.description or 'N/A',
           self.author or 'N/A',
           '\n'.join(parts_info),
           interactions_info or 'N/A',
           constraints_info or 'N/A',
           bc_info or 'N/A'
           )
        print(data)
        return data

    # ==============================================================================
    # Save model file
    # ==============================================================================

    def check(self, type='quick'):
        """Check for possible problems in the model

            Warning
            -------
            WIP! It is better if you check yourself...

            Parameters
            ----------
            type : str, optional
                *quick* or *deep* check, by default 'quick'

            Returns
            -------
            str
                report
            """

        def _check_units(self):
            """Check if the units are consistent.
            """
            raise NotImplementedError

        def _check_bcs(self):
            """Check if the units are consistent.
            """
            raise NotImplementedError

        raise NotImplementedError

    # ==============================================================================
    # Viewer
    # ==============================================================================
    def show(self, width=1600, height=900, scale_factor=1., parts=None,
             draw_elements=True, draw_nodes=False, node_labels=False,
             draw_bcs=1., **kwargs):

        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.geometry import Point, Vector
        import numpy as np

        from compas.colors import ColorMap, Color
        cmap = ColorMap.from_mpl('viridis')

        parts = parts or self.parts

        v = FEA2Viewer(width, height, scale_factor)

        v.draw_parts(parts,
                     draw_elements,
                     draw_nodes,
                     node_labels)

        if draw_bcs:
            v.draw_bcs(self, parts, draw_bcs)

        v.show()
