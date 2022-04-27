from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# import pickle
# import os
import importlib

# import compas_fea2
from compas_fea2 import config

from compas_fea2.base import FEAData
from compas_fea2.model.parts import Part
from compas_fea2.model.nodes import Node
from compas_fea2.model.materials import _Material, material
from compas_fea2.model.sections import _Section
from compas_fea2.model.bcs import BoundaryCondition
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import ElementsGroup
from compas_fea2.model.groups import FacesGroup
from compas_fea2.model.interfaces import Interface
from compas_fea2.model.constraints import _Constraint
from compas_fea2.model.bcs import BoundaryCondition


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
    materials : Set[:class:`compas_fea2.model._Material`]
        The materials of the model.
    sections : Set[:class:`compas_fea2.model._Section`]
        The sections used in the model.
    bcs : dict
        The boundary conditions of the model.
    constraints : Set[:class:`compas_fea2.model._Constraint`]
        The constraints of the model.
    interactions : Set[:class:`compas_fea2.model._Interaction`]
        The interactions between parts of the model.
    contacts : Set[:class:`compas_fea2.model._Contact`]
        The contacts between parts of the model.
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
        self._contacts = set()
        self._partsgroups = set()
        self._facesgroups = set()

    @property
    def parts(self):
        return self._parts

    @property
    def materials(self):
        return self._materials

    @property
    def sections(self):
        return self._sections

    @property
    def partgroups(self):
        return self._partsgroups

    @property
    def bcs(self):
        return self._bcs

    @property
    def contacts(self):
        return self._contacts

    @property
    def constraints(self):
        return self._constraints

    @property
    def interactions(self):
        return self._interactions

    @property
    def facesgroups(self):
        return self._facesgroups

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    # @classmethod
    # def from_compas_assembly(cls, name, assembly, mesh_size, section, contact):
    #     from compas_fea2.preprocessor.meshing import compas_to_gmsh_3d
    #     from compas_fea2.utilities.interfaces import nodes_on_plane, elements_on_plane
    #     from compas.geometry import Plane
    #     from compas.datastructures import mesh_weld
    #     # import compas_gmsh
    #     from compas_gmsh.models import MeshModel

    #     gmshModel = MeshModel()

    #     # m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))

    #     model = cls(name=name)

    #     blocks = [assembly.node_attribute(node, 'block') for node in assembly.nodes()]

    #     for i, block in enumerate(blocks):
    #         # block = mesh_weld(block)
    #         # gmshModel.from_mesh(block)
    #         # mesh = gmshModel.mesh_to_compas()
    #         # gmshModel.synchronize()
    #         # gmshModel.generate_mesh(3)
    #         # part = m.Part.from_gmsh(name=f'block-{i}', gmshModel=gmshModel, section=section)
    #         if mesh_size:
    #             meshModel = compas_to_gmsh_3d(block, mesh_size)
    #             part = Part.from_gmsh(name=f'block-{i}', gmshModel=meshModel, section=section)
    #         else:
    #             part = Part.from_compas_mesh(name=f'block-{i}', mesh=block, section=section)
    #         model.add_part(part)

    #     first_block = list(model.parts.values())[0]
    #     last_block = list(model.parts.values())[-1]

    #     supp_a = nodes_on_plane(first_block, Plane([0, 0, 0], [0, 0, 1]))
    #     supp_b = nodes_on_plane(last_block, Plane([0, 0, 0], [0, 0, 1]))
    #     model.add_fix_bc(name='left_support', part=first_block, where=supp_a)
    #     model.add_fix_bc(name='right_support', part=last_block, where=supp_b)

    #     blocks_interface = [assembly.edge_attribute(edge, 'interface') for edge in assembly.edges()]
    #     for i, interface in enumerate(blocks_interface):
    #         if i == len(blocks):
    #             break
    #         master = elements_on_plane(model.parts[f'block-{i}'], Plane.from_frame(interface.frame))
    #         slave = elements_on_plane(model.parts[f'block-{i+1}'], Plane.from_frame(interface.frame))
    #         model.add_contact(ContactPair(master=FacesGroup(name=f'master_{i}_{i+1}',
    #                                                         part=f'block-{i}',
    #                                                         element_face=master),
    #                                       slave=FacesGroup(name=f'slave_{i}_{i+1}',
    #                                                        part=f'block-{i+1}',
    #                                                        element_face=slave),
    #                                       interaction=contact))

    #     return model

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def find_parts_by_name(self, name):
        # type: (str) -> Part
        """Find all the parts with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Part`]

        """
        return [part for part in self.parts if part.name == name]

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
    #                           Groups methods
    # =========================================================================

    # # NOTE: Nodes and Elements groups should not be added but defined (similarly to what happens for Parts)
    # def add_group(self, group, part):
    #     """Add a Group object to a part in the Model. it can be either a
    #     :class:`NodesGroup` or an :class:`ElementsGroup`.

    #     Parameters
    #     ----------
    #     group : obj
    #         :class:`NodesGroup` or :class:`ElementsGroup` object to add.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.

    #     Returns
    #     -------
    #     None
    #     """
    #     part = self._check_part_in_model(part)
    #     part.add_group(group)

    # def add_partgroups(self, groups, part):
    #     """Add multiple Group objects to a part in the Model. Can be
    #     a list of NodesGroup or ElementsGroup objects, also mixed.

    #     Parameters
    #     ----------
    #     group : obj
    #         group object.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.

    #     Returns
    #     -------
    #     None
    #     """
    #     for group in groups:
    #         self.add_group(group, part)

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
            self._contacts.add(interface)
        else:
            raise TypeError('{!r} is not an interface.'.format(interface))
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

    # TODO implement NodesGroup assignment
    def add_bc(self, bc, node):
        # type: (BoundaryCondition, Node) -> BoundaryCondition
        """Add a :class:`compas_fea2.model.BoundaryCondition` to the model.

        Note
        ----
        Currently global axes are used in the Boundary Conditions definition.

        Parameters
        ----------
        bc : :class:`compas_fea2.model.BoundaryCondition`
            Boundary condition object to add to the model.
        node : :class:`compas_fea2.model.Node
            Node where the boundary condition is applied.

        Returns
        -------
        None

        """
        if not isinstance(node, Node):
            raise TypeError('{!r} is not a Node.'.format(node))

        if not isinstance(bc, BoundaryCondition):
            raise TypeError('{!r} is not a BoundaryCondition.'.format(bc))

        # self.contains_node(node) #TODO implement method
        node.dof = bc
        self._bcs.setdefault(node.part, {}).setdefault(bc, set()).add(node)
        return bc

    def add_bcs(self, bc, nodes):
        # type: (BoundaryCondition, list) -> list
        """Add a :class:`compas_fea2.model.BoundaryCondition` objects to
        multiple nodes.

        Parameters
        ----------
        bc : :class:`compas_fea2.model.BoundaryCondition`
            Boundary condition object to add to the model.
        nodes : list[:class:`compas_fea2.model.Node`]
            List with the nodes where the boundary condition is assigned.

        Returns
        -------
        list[:class:`compas_fea2.model.BoundaryCondition`]
        """
        return [self.add_bc(bc, node) for node in nodes]

    def _add_bc_type(self, bc_type, node, axes='global'):
        # type: (str, Node, str) -> BoundaryCondition
        """Add a :class:`compas_fea2.model.BoundaryCondition` by type.

        Note
        ----
        The bc_type must be one of the following:

        .. csv-table::
            :header: bc_type , BC

            fix, :class:`compas_fea2.model.bcs.FixedBC`
            fixXX, :class:`compas_fea2.model.bcs.FixedBCXX`
            fixYY, :class:`compas_fea2.model.bcs.FixedBCYY`
            fixZZ, :class:`compas_fea2.model.bcs.FixedBCZZ`
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
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
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
        return self.add_bc(bc, node)

    def add_fix_bc(self, node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a :class:`compas_fea2.model.FixedBC` to the nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('fix', node, axes)

    def add_fixXX_bc(self, node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a fixed boundary condition type free about XX to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('fixXX', node, axes)

    def add_fixYY_bc(self, node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a fixed boundary condition free about YY type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('fixYY', node, axes)

    def add_fixZZ_bc(self, node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a fixed boundary condition free about ZZ type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('fixZZ', node, axes)

    def add_pin_bc(self, node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a pinned boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('pin', node, axes)

    def add_rollerX_bc(self,  node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a roller free on X boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerX',  node, axes)

    def add_rollerY_bc(self,  node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a roller free on Y boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerY',  node, axes)

    def add_rollerZ_bc(self,  node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a roller free on Z boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerZ', node, axes)

    def add_rollerXY_bc(self,  node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a roller free on XY boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerXY',  node, axes)

    def add_rollerXZ_bc(self,  node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a roller free on XZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerXZ',  node, axes)

    def add_rollerYZ_bc(self,  node, axes='global'):
        # type: (Node, str) -> BoundaryCondition
        """Add a roller free on YZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        node : :class:`copmpas_fea2.model.nodes.Node`
            Node to apply the boundary condition to.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        return self._add_bc_type('rollerYZ',  node, axes)

    def remove_bc(self, bc):
        """Removes a boundary condition from the Model.

        Parameters
        ----------
        bc_name : str
            Name of thedisplacement to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

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
        bc_info = '\n'.join(['{}: \n{}'.format(part.name, '\n'.join(['  {!r} - {!r}'.format(bc, [node for node in nodes])
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
           ''.join(parts_info),
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
    def show(self, width=800, height=500, scale_factor=1, node_labels=None):
        from compas_fea2.UI.viewer import ModelViewer
        v = ModelViewer(self, width, height, scale_factor, node_labels)
        v.show()

    # def save_to_cfm(self, path, output=True):
    #     """Exports the Model object to an .cfm file through Pickle.

    #     Parameters
    #     ----------
    #     path : path
    #         Path to the folder where save the file to.
    #     output : bool
    #         Print terminal output.

    #     Returns
    #     -------
    #     None
    #     """

    #     if not os.path.exists(path):
    #         os.makedirs(path)

    #     filename = '{0}/{1}.cfm'.format(path, self.name)

    #     with open(filename, 'wb') as f:
    #         pickle.dump(self, f)

    #     if output:
    #         print('***** Model saved to: {0} *****\n'.format(filename))

    # # ==============================================================================
    # # Load model file
    # # ==============================================================================

    # @ staticmethod
    # def load_from_cfm(filename, output=True):
    #     """Imports a Model object from an .cfm file through Pickle.

    #     Parameters
    #     ----------
    #     filename : str
    #         Path to load the Model .cfm from.
    #     output : bool
    #         Print terminal output.

    #     Returns
    #     -------
    #     obj
    #         Imported Model object.
    #     """
    #     with open(filename, 'rb') as f:
    #         mdl = pickle.load(f)

    #     if output:
    #         print('***** Model loaded from: {0} *****'.format(filename))

    #     return mdl
