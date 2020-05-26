from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

from compas.geometry import centroid_points
from compas.utilities import geometric_key

from compas_fea2.utilities import group_keys_by_attribute
from compas_fea2.utilities import group_keys_by_attributes

from compas_fea2.backends._core.components.elements import *

from compas_fea2.backends._core.components.properties import ElementPropertiesBase
from compas_fea2.backends._core.components.loads import LoadBase
from compas_fea2.backends._core.components.loads import ThermalLoadBase
from compas_fea2.backends._core.components.bcs import GeneralDisplacementBase
from compas_fea2.backends._core.components.materials import MaterialBase
from compas_fea2.backends._core.components.sections import SectionBase
from compas_fea2.backends._core.components.steps import StepBase


__all__ = [
    'StructureBase',
]


# this makes really very little sense
# it is only here to be able to provide string names for types
# but i will leave it for now and refactor one thing at a time...
ETYPES = {
    'BeamElement':        BeamElementBase,
    'SpringElement':      SpringElementBase,
    'TrussElement':       TrussElementBase,
    'StrutElement':       StrutElementBase,
    'TieElement':         TieElementBase,
    'ShellElement':       ShellElementBase,
    'MembraneElement':    MembraneElementBase,
    'FaceElement':        FaceElementBase,
    'SolidElement':       SolidElementBase,
    'TetrahedronElement': TetrahedronElementBase,
    'PentahedronElement': PentahedronElementBase,
    'HexahedronElement':  HexahedronElementBase,
    'MassElement':        MassElementBase
}


class StructureBase(object):
    """Initialises Structure object for use in finite element analysis.

    Parameters
    ----------
    path : str
        Path to save all compas_fea associated files.
    name : str
        Name of the structure.

    Attributes
    ----------
    constraints : dict
        Constraint objects.
    displacements : dict
        Displacement objects.
    elements : dict
        Element objects.
    element_index : dict
        Index of elements (element centroid geometric keys).
    element_properties : dict
        ElementProperties objects.
    interactions : dict
        Interaction objects.
    loads : dict
        Load objects.
    materials : dict
        Material objects.
    misc : dict
        Misc objects.
    name : str
        Structure name.
    nodes : dict
        Node objects.
    node_index : dict
        Index of nodes (node geometric keys).
    path : str
        Path to save files.
    results : dict
        Dictionary containing analysis results.
    sections : dict
        Section objects.
    sets : dict
        Set objects.
    steps : dict
        Step objects.
    steps_order : list
        Sorted list of Step object names.
    tol : str
        Geometric key tolerance.
    virtual_nodes : dict
        Node objects for virtual nodes.
    virtual_elements : dict
        Element objects for virtual elements.
    virtual_element_index : dict
        Index of virtual elements (element centroid geometric keys).
    """

    def __init__(self, path, name='compas_fea-Structure'):
        self.constraints           = {}
        self.displacements         = {}
        self.elements              = {}
        self.element_index         = {}
        self.element_properties    = {}
        self.interactions          = {}
        self.loads                 = {}
        self.materials             = {}
        self.misc                  = {}
        self.name                  = name
        self.nodes                 = {}
        self.node_index            = {}
        self.path                  = path
        self.results               = {}
        self.sections              = {}
        self.steps                 = {}
        self.steps_order           = []
        self.tol                   = '3'
        self.virtual_nodes         = {}
        self.virtual_node_index    = {}
        self.virtual_elements      = {}
        self.virtual_element_index = {}

    def __str__(self):
        n = self.node_count()
        m = self.element_count()
        data = [
            self.materials,
            self.sections,
            self.loads,
            self.displacements,
            self.constraints,
            self.interactions,
            self.misc,
            self.steps]
        d = []
        for entry in data:
            if entry:
                d.append('\n'.join(['  {0} : {1}'.format(i, j.__name__) for i, j in entry.items()]))
            else:
                d.append('n/a')
        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea Structure: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Nodes
-----
{}

Elements
--------
{}

Materials
---------
{}

Sections
--------
{}

Loads
-----
{}

Displacements
-------------
{}

Constraints
-----------
{}

Interactions
------------
{}

Misc
----
{}

Steps
-----
{}

""".format(self.name, n, m, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

    # ==============================================================================
    # Nodes
    # ==============================================================================

    def check_node_exists(self, xyz):
        """Check if a node already exists at given x, y, z co-ordinates.

        Parameters
        ----------
        xyz : list
            [x, y, z] co-ordinates of node to check.

        Returns
        -------
        int
            The node index if the node already exists, None if not.

        Notes
        -----
        Geometric key check is made according to self.tol [m] tolerance.
        """
        xyz = [float(i) for i in xyz]
        return self.node_index.get(geometric_key(xyz, '{0}f'.format(self.tol)), None)

    # it would make more sense if a node has a local frame
    # instead of ex, ey, ez
    # are the coordinates with respect to the local axes?
    def add_node(self, xyz, ex=[1, 0, 0], ey=[0, 1, 0], ez=[0, 0, 1], mass=0, virtual=False):
        """Adds a node to structure.nodes at co-ordinates xyz with local frame [ex, ey, ez].

        Parameters
        ----------
        xyz : list
            [x, y, z] co-ordinates of the node.
        ex : list
            Node's local x axis.
        ey : list
            Node's local y axis.
        ez : list
            Node's local z axis.
        mass : float
            Lumped mass at node.
        virtual: bool
            Is the node virtual.

        Returns
        -------
        int
            Key of the added or pre-existing node.

        Notes
        -----
        Nodes are numbered sequentially starting from 0.
        """
        xyz = [float(axis) for axis in xyz]
        key = self.check_node_exists(xyz)
        if key is None:
            key = self.node_count()
            self.nodes[key] = NodeBase(key=key, xyz=xyz, ex=ex, ey=ey, ez=ez, mass=mass)
            if virtual:
                self.add_node_to_node_index(key=key, xyz=xyz, virtual=True)
            else:
                self.add_node_to_node_index(key=key, xyz=xyz)
        return key

    # again, using a frame would make more sense
    def add_nodes(self, nodes, ex=[1, 0, 0], ey=[0, 1, 0], ez=[0, 0, 1]):
        """Adds a list of nodes to structure.nodes at given co-ordinates all with local frame [ex, ey, ez].

        Parameters
        ----------
        nodes : list
            [[x, y, z], ..] co-ordinates for each node.
        ex : list
            Nodes' local x axis.
        ey : list
            Nodes' local y axis.
        ez : list
            Nodes' local z axis.

        Returns
        -------
        list
            Keys of the added or pre-existing nodes.

        Notes
        -----
        Nodes are numbered sequentially starting from 0.
        """
        return [self.add_node(xyz=xyz, ex=ex, ey=ey, ez=ez) for xyz in nodes]

    def add_node_to_node_index(self, key, xyz, virtual=False):
        """Adds the node to the node_index dictionary.

        Parameters
        ----------
        key : int
            Prescribed node key.
        xyz : list
            [x, y, z] co-ordinates of the node.
        virtual: bool
            Is the node virtual or not.

        Returns
        -------
        None
        """
        gkey = geometric_key(xyz, '{0}f'.format(self.tol))
        if virtual:
            self.virtual_node_index[gkey] = key
        else:
            self.node_index[gkey] = key

    def edit_node(self, key, attr_dict):
        """Edit the data of a node.

        Parameters
        ----------
        key : int
            Key of the node to edit.
        attr_dict : dict
            Attribute dictionary of data to edit.

        Returns
        -------
        None
        """
        gkey = geometric_key(self.node_xyz(key), '{0}f'.format(self.tol))
        del self.node_index[gkey]
        for attr, item in attr_dict.items():
            setattr(self.nodes[key], attr, item)
        self.add_node_to_node_index(key, self.node_xyz(key))

    def node_bounds(self):
        """Return the bounds formed by the Structure's nodal co-ordinates.

        Parameters
        ----------
        None

        Returns
        -------
        list
            [xmin, xmax].
        list
            [ymin, ymax].
        list
            [zmin, zmax].
        """
        n = self.node_count()
        x = [0] * n
        y = [0] * n
        z = [0] * n
        for c, node in self.nodes.items():
            x[c] = node.x
            y[c] = node.y
            z[c] = node.z
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        zmin, zmax = min(z), max(z)
        return [xmin, xmax], [ymin, ymax], [zmin, zmax]

    def node_count(self):
        """Return the number of nodes in the Structure.

        Parameters
        ----------
        None

        Returns
        -------
        int
            Number of nodes stored in the Structure object.
        """
        return len(self.nodes) + len(self.virtual_nodes)

    def node_xyz(self, node):
        """Return the xyz co-ordinates of a node.

        Parameters
        ----------
        node : int
            Node number.

        Returns
        -------
        list
            [x, y, z] co-ordinates.
        """
        return [getattr(self.nodes[node], i) for i in 'xyz']

    def nodes_xyz(self, nodes=None):
        """Return the xyz co-ordinates of given or all nodes.

        Parameters
        ----------
        nodes : list
            Node numbers, give None for all nodes.

        Returns
        -------
        list
            [[x, y, z] ...] co-ordinates.
        """
        if nodes is None:
            nodes = sorted(self.nodes, key=int)

        return [self.node_xyz(node=node) for node in nodes]

    # ==============================================================================
    # Elements
    # ==============================================================================

    # i think passing the element type as a string is a really bad idea
    # and seems only necessary for adding stuff from Rhino
    # the class
    # or even better the object
    # could be passed as a parameter
    # there also seems no difference in the handling of different element
    # so the element might as well be created externally
    def add_element(self, nodes, etype, thermal=False, axes={}, mass=None):
        """Adds an element to structure.elements with centroid geometric key.

        Parameters
        ----------
        nodes : list
            Nodes the element is connected to.
        etype : str
            Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez'.
        mass : float
            Element mass.

        Returns
        -------
        int
            Key of the added or existing element.

        Notes
        -----
        Elements are numbered sequentially starting from 0.
        """
        if len(nodes) == len(set(nodes)):
            ekey = self.check_element_exists(nodes)
            if ekey is None:
                ekey                = self.element_count()
                element             = ETYPES[etype]()
                element.axes        = axes
                element.nodes       = nodes
                element.number      = ekey
                element.thermal     = thermal
                element.mass        = mass
                self.elements[ekey] = element
                self.add_element_to_element_index(ekey, nodes)
            return ekey
        return None

    def add_elements(self, elements, type, thermal=False, axes={}):
        """Adds multiple elements of the same type to structure.elements.

        Parameters
        ----------
        elements : list
            List of lists of the nodes the elements are connected to.
        type : str
            Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez' for all elements.

        Returns
        -------
        list
            Keys of the added or existing elements.

        Notes
        -----
        Elements are numbered sequentially starting from 0.
        """
        return [self.add_element(nodes=nodes, type=type, thermal=thermal, axes=axes) for nodes in elements]

    def add_element_to_element_index(self, key, nodes, virtual=False):
        """Adds the element to the element_index dictionary.

        Parameters
        ----------
        key : int
            Prescribed element key.
        nodes : list
            Node numbers the element is connected to.
        virtual: bool
            If true, adds element to the virtual_element_index dictionary.

        Returns
        -------
        None
        """
        centroid = centroid_points([self.node_xyz(node) for node in nodes])
        gkey     = geometric_key(centroid, '{0}f'.format(self.tol))
        if virtual:
            self.virtual_element_index[gkey] = key
        else:
            self.element_index[gkey] = key

    def check_element_exists(self, nodes=None, xyz=None, virtual=False):
        """Check if an element already exists based on nodes or centroid.

        Parameters
        ----------
        nodes : list
            Node numbers the element is connected to.
        xyz : list
            Direct co-ordinates of the element centroid to check.
        virtual: bool
            Is the element to be checked a virtual element.

        Returns
        -------
        int
            The element index if the element already exists, None if not.

        Notes
        -----
        Geometric key check is made according to self.tol [m] tolerance.
        """
        if not xyz:
            xyz = centroid_points([self.node_xyz(node) for node in nodes])
        gkey = geometric_key(xyz, '{0}f'.format(self.tol))
        if virtual:
            return self.virtual_element_index.get(gkey, None)
        else:
            return self.element_index.get(gkey, None)

    def edit_element(self):
        raise NotImplementedError

    def element_count(self):
        """Return the number of elements in the Structure.

        Parameters
        ----------
        None

        Returns
        -------
        int
            Number of elements stored in the Structure object.
        """
        return len(self.elements) + len(self.virtual_elements)

    def element_centroid(self, element):
        """Return the centroid of an element.

        Parameters
        ----------
        element : int
            Number of the element.

        Returns
        -------
        list
            Co-ordinates of the element centroid.
        """
        return centroid_points(self.nodes_xyz(nodes=self.elements[element].nodes))

    def add_nodal_element(self, node, type, virtual_node=False):
        """Adds a nodal element to structure.elements with the possibility of
        adding a coincident virtual node. Virtual nodes are added to a node
        set called 'virtual_nodes'.

        Parameters
        ----------
        node : int
            Node number the element is connected to.
        type : str
            Element type: 'SpringElement'.
        virtual_node : bool
            Create a virtual node or not.

        Returns
        -------
        int
            Key of the added element.

        Notes
        -----
        Elements are numbered sequentially starting from 0.
        """
        if virtual_node:
            xyz = self.node_xyz(node)
            key = self.virtual_nodes.setdefault(node, self.node_count())
            self.nodes[key] = {'x': xyz[0], 'y': xyz[1], 'z': xyz[2],
                               'ex': [1, 0, 0], 'ey': [0, 1, 0], 'ez': [0, 0, 1], 'virtual': True}
            if 'virtual_nodes' in self.collections:
                self.collections['virtual_nodes']['selection'].append(key)
            else:
                self.collections['virtual_nodes'] = {'type': 'node', 'selection': [key], 'explode': False}
            nodes = [node, key]
        else:
            nodes = [node]

        func_dict = {
            'SpringElement': SpringElement,
        }

        ekey = self.element_count()
        element = func_dict[type]()
        element.nodes = nodes
        element.number = ekey
        self.elements[ekey] = element
        return ekey

    def add_virtual_element(self, nodes, type, thermal=False, axes={}):
        """Adds a virtual element to structure.elements and to element set 'virtual_elements'.

        Parameters
        ----------
        nodes : list
            Nodes the element is connected to.
        type : str
            Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez'.

        Returns
        -------
        int
            Key of the added virtual element.

        Notes
        -----
        Virtual elements are numbered sequentially starting from 0.
        """
        ekey = self.check_element_exists(nodes, virtual=True)

        if ekey is None:

            ekey            = self.element_count()
            element         = func_dict[type]()
            element.axes    = axes
            element.nodes   = nodes
            element.number  = ekey
            element.thermal = thermal

            self.virtual_elements[ekey] = element
            self.add_element_to_element_index(ekey, nodes, virtual=True)

            if 'virtual_elements' in self.sets:
                self.collections['virtual_elements']['selection'].append(ekey)
            else:
                self.collections['virtual_elements'] = {'type': 'virtual_element', 'selection': [ekey],
                                                 'index': len(self.sets)}

        return ekey

    def assign_element_property(self, element_property):
        """Assign the ElementProperties object name to associated Elements.

        Parameters
        ----------
        element_property : obj
            ElementProperties object.

        Returns
        -------
        None
        """
        if element_property.collection:
            elements = self.collections[element_property.collection].selection
        else:
            elements = element_property.elements

        for element in elements:
            self.elements[element].element_property = element_property.name

    # ==============================================================================
    # Nodes and Elements
    # ==============================================================================

    def add_nodes_elements_from_mesh(self, mesh, element_type, thermal=False):
        """Adds the nodes and faces of a Mesh to the Structure object.

        Parameters
        ----------
        mesh : obj
            Mesh datastructure object.
        element_type : str
            Element type: 'ShellElement', 'MembraneElement' etc.
        thermal : bool
            Thermal properties on or off.

        Returns
        -------
        list
            Keys of the created elements.
        """
        for key in sorted(list(mesh.vertices()), key=int):
            self.add_node(mesh.vertex_coordinates(key))
        ekeys = []
        for fkey in list(mesh.faces()):
            face = [self.check_node_exists(mesh.vertex_coordinates(i)) for i in mesh.face[fkey]]
            ekeys.append(self.add_element(nodes=face, type=element_type, thermal=thermal))
        return ekeys

    def add_nodes_elements_from_network(self, network, element_type, thermal=False, axes={}):
        """Adds the nodes and edges of a Network to the Structure object.

        Parameters
        ----------
        network : obj
            Network datastructure object.
        element_type : str
            Element type: 'BeamElement', 'TrussElement' etc.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez' for all elements.

        Returns
        -------
        list
            Keys of the created elements.
        """
        for key in sorted(list(network.nodes()), key=int):
            self.add_node(network.node_coordinates(key))
        ekeys = []
        for u, v in list(network.edges()):
            sp = self.check_node_exists(network.node_coordinates(u))
            ep = self.check_node_exists(network.node_coordinates(v))
            ekeys.append(self.add_element(nodes=[sp, ep], type=element_type, thermal=thermal, axes=axes))
        return ekeys

    def add_nodes_elements_from_volmesh(self, volmesh, element_type='SolidElement', thermal=False, elset=None, axes={}):
        """Adds the nodes and cells of a VolMesh to the Structure object.

        Parameters
        ----------
        volmesh : obj
            VolMesh datastructure object.
        element_type : str
            Element type: 'SolidElement' or ....
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez' for all elements.

        Returns
        -------
        list
            Keys of the created elements.
        """
        for key in sorted(list(volmesh.vertices()), key=int):
            self.add_node(volmesh.vertex_coordinates(key))

        ekeys = []

        for ckey in volmesh.cell:
            cell_vertices = volmesh.cell_vertices(ckey)
            nkeys = [self.check_node_exists(volmesh.vertex_coordinates(nk)) for nk in cell_vertices]
            ekeys.append(self.add_element(nodes=nkeys, type=element_type, acoustic=acoustic, thermal=thermal,axes=axes))

        return ekeys

    # ==============================================================================
    # Components
    # adding and retrieving elements/components should not rely
    # on the user providing unique names
    # there should be some mechanism based on (GU)IDs
    # add functions should return that ID
    # ==============================================================================

    # again
    # seems like a bad idea
    # except via the implementation
    # one has no way of knowing that this is only relevant
    # for "components"
    # it also constantly needs to be updated to add support for new "components"
    def add(self, objects):
        """Adds object(s) to their correct attribute dictionary in the structure.

        Parameters
        ----------
        objects : obj, list
            The object or list of objects to add.

        Returns
        -------
        None
        """
        if not isinstance(objects, list):
            objects = [objects]

        for obj in objects:
            # cl = i.__class__
            # if issubclass(cl, MaterialBase):
            #     self.add_material(i)
            # elif issubclass(cl, SectionBase):
            #     self.add_section(i)
            # elif isinstance(i, ElementPropertiesBase):
            #     self.add_element_properties(i)
            # elif issubclass(cl, GeneralDisplacementBase) or isinstance(i, GeneralDisplacementBase):
            #     self.add_displacement(i)
            # elif issubclass(cl, LoadBase) or isinstance(i, ThermalLoadBase):
            #     self.add_load(i)
            # elif issubclass(cl, StepBase):
            #     self.add_step(i)
            if isinstance(obj, MaterialBase):
                self.add_material(obj)
            elif isinstance(obj, SectionBase):
                self.add_section(obj)
            elif isinstance(obj, ElementPropertiesBase):
                self.add_element_properties(obj)
            elif isinstance(obj, GeneralDisplacementBase):
                self.add_displacement(obj)
            elif isinstance(obj, LoadBase):
                self.add_load(obj)
            elif isinstance(obj, StepBase):
                self.add_step(obj)
            else:
                raise NotImplementedError
                # print('***** WARNING: object type not found using structure.add() *****')

    def add_constraint(self, constraint):
        """Adds a Constraint object to structure.constraints.

        Parameters
        ----------
        constraint : obj
            The Constraint object.

        Returns
        -------
        None
        """
        constraint.index = len(self.constraints)
        self.constraints[constraint.name] = constraint

    def add_displacement(self, displacement):
        """Adds a Displacement object to structure.displacements.

        Parameters
        ----------
        displacement : obj
            The Displacement object.

        Returns
        -------
        None
        """
        displacement.index = len(self.displacements)
        self.displacements[displacement.name] = displacement

    def add_displacements(self, displacements):
        """Adds Displacement objects to structure.displacements.

        Parameters
        ----------
        displacements : list
            The Displacement objects.

        Returns
        -------
        None
        """
        for displacement in displacements:
            self.add_displacement(displacement)

    def add_element_properties(self, element_properties):
        """Adds ElementProperties object(s) to structure.element_properties.

        Parameters
        ----------
        element_properties : obj, list
            The ElementProperties object(s).

        Returns
        -------
        None
        """
        if isinstance(element_properties, list):
            for element_property in element_properties:
                element_property.index = len(self.element_properties)
                self.element_properties[element_property.name] = element_property
                self.assign_element_property(element_property)
        else:
            print(element_properties)
            element_properties.index = len(self.element_properties)
            self.element_properties[element_properties.name] = element_properties
            self.assign_element_property(element_properties)

    def add_interaction(self, interaction):
        """Adds an Interaction object to structure.interactions.

        Parameters
        ----------
        interaction : obj
            The Interaction object.

        Returns
        -------
        None
        """
        interaction.index = len(self.interactions)
        self.interactions[interaction.name] = interaction

    def add_load(self, load):
        """Adds a Load object to structure.loads.

        Parameters
        ----------
        load : obj
            The Load object.

        Returns
        -------
        None
        """
        load.index = len(self.loads)
        self.loads[load.name] = load

    def add_loads(self, loads):
        """Adds Load objects to structure.loads.

        Parameters
        ----------
        loads : list
            The Load objects.

        Returns
        -------
        None
        """
        for load in loads:
            self.add_load(load)

    def add_material(self, material):
        """Adds a Material object to structure.materials.

        Parameters
        ----------
        material : obj
            The Material object.

        Returns
        -------
        None
        """
        material.index = len(self.materials)
        self.materials[material.name] = material

    def add_materials(self, materials):
        """Adds Material objects to structure.materials.

        Parameters
        ----------
        materials : list
            The Material objects.

        Returns
        -------
        None
        """
        for material in materials:
            self.add_material(material)

    def add_misc(self, misc):
        """Adds a Misc object to structure.misc.

        Parameters
        ----------
        misc : obj
            The Misc object.

        Returns
        -------
        None
        """
        misc.index = len(self.misc)
        self.misc[misc.name] = misc

    def add_section(self, section):
        """Adds a Section object to structure.sections.

        Parameters
        ----------
        section : obj
            The Section object.

        Returns
        -------
        None
        """
        section.index = len(self.sections)
        self.sections[section.name] = section

    def add_sections(self, sections):
        """Adds Section objects to structure.sections.

        Parameters
        ----------
        sections : list
            The Section objects.

        Returns
        -------
        None
        """
        for section in sections:
            self.add_section(section)

    def add_step(self, step):
        """Adds a Step object to structure.steps.

        Parameters
        ----------
        step : obj
            The Step object.

        Returns
        -------
        None
        """
        step.index = len(self.steps)
        self.steps[step.name] = step

    def add_steps(self, steps):
        """Adds Step objects to structure.steps.

        Parameters
        ----------
        steps : list
            The Step objects.

        Returns
        -------
        None
        """
        for step in steps:
            self.add_step(step)

    # ==============================================================================
    # Modifiers
    # ==============================================================================

    def scale_displacements(self, displacements, factor):
        """Scales displacements by a given factor.

        Parameters
        ----------
        displacements : dict
            Dictionary containing the displacements to scale.
        factor : float
            Factor to scale the displacements by.

        Returns
        -------
        dict
            The scaled displacements dictionary.
        """
        disp_dic = {}

        for key, disp in displacements.items():
            for dkey, dcomp in disp.components.items():
                if dcomp is not None:
                    disp.components[dkey] *= factor
            disp_dic[key] = disp

        return disp_dic

    def scale_loads(self, loads, factor):
        """Scales loads by a given factor.

        Parameters
        ----------
        loads : dict
            Dictionary containing the loads to scale.
        factor : float
            Factor to scale the loads by.

        Returns
        -------
        dict
            The scaled loads dictionary.
        """
        loads_dic = {}

        for key, load in loads.items():
            for lkey, lcomp in load.components.items():
                if lcomp is not None:
                    load.components[lkey] *= factor
            loads_dic[key] = load

        return loads_dic

    # ==============================================================================
    # Steps
    # ==============================================================================

    def set_steps_order(self, order):
        """Sets the order that the Steps will be analysed.

        Parameters
        ----------
        order : list
            An ordered list of the Step names.

        Returns
        -------
        None
        """
        self.steps_order = order

    # ==============================================================================
    # Results
    # ==============================================================================

    def get_nodal_results(self, step, field, nodes='all'):
        """Extract nodal results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        nodes : str, list
            Extract 'all' or a node collection/list.

        Returns
        -------
        dict
            The nodal results for the requested field.
        """
        data  = {}
        rdict = self.results[step]['nodal']

        if nodes == 'all':
            keys = list(self.nodes.keys())
        else:
            keys = nodes

        for key in keys:
            data[key] = rdict[field][key]

        return data

    def get_element_results(self, step, field, elements='all'):
        """Extract element results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        elements : str, list
            Extract 'all' or an element collection/list.

        Returns
        -------
        dict
            The element results for the requested field.
        """
        data  = {}
        rdict = self.results[step]['element']

        if elements == 'all':
            keys = list(self.elements.keys())

        # elif isinstance(elements, str):              TODO: transfor to 'collection'
        #     keys = self.sets[elements].selection

        else:
            keys = elements

        for key in keys:
            data[key] = rdict[field][key]

        return data

    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        """Prints a summary of the Structure object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(self)

    # ==============================================================================
    # Save
    # ==============================================================================

    def save_to_cfea(self, output=True):
        """Exports the Structure object to an .obj file through Pickle.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """
        filename = os.path.join(self.path, self.name + '.cfea')

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print('***** Structure saved to: {0} *****\n'.format(filename))

    # ==============================================================================
    # Load
    # ==============================================================================

    @staticmethod
    def load_from_cfea(filename, output=True):
        """Imports a Structure object from an .obj file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Structure .obj from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Structure object.
        """
        with open(filename, 'rb') as f:
            structure = pickle.load(f)

        if output:
            print('***** Structure loaded from: {0} *****'.format(filename))

        return structure
