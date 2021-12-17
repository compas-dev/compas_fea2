from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import importlib

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.model.materials import MaterialBase
from compas_fea2.backends._base.model.sections import SectionBase
from compas_fea2.backends._base.model.groups import NodesGroupBase
from compas_fea2.backends._base.model.groups import ElementsGroupBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'PartBase',
]


class PartBase(FEABase):
    """Base Part object.

    Parameters
    ----------
    name : str
        Name of the `Part`.
    """

    def __init__(self, name):
        self.__name__ = 'Part'
        self._name = name

        self._nodes = []
        self._nodes_gkeys = []

        self._materials = {}
        self._sections = {}

        self._elements = {}
        self._groups = {}
        self._releases = {}

    @property
    def name(self):
        """str : Name of the `Part`"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def nodes(self):
        """list : Sorted list (by Node key) with the `Nodes` objects belonging to the Part."""
        return self._nodes

    @property
    def materials(self):
        """dict : Dictionary with the `Material` objects belonging to the Part."""
        return self._materials

    @property
    def sections(self):
        """dict : Dictionary with the `Section` objects belonging to the Part."""
        return self._sections

    @property
    def elements(self):
        """dict : Sorted list (by `Element key`) with the `Element` objects belonging to the Part."""
        return self._elements

    @property
    def groups(self):
        """list : List with the `NodesGroup` or `ElementsGroup` objects belonging to the `Part`."""
        return self._groups

    @property
    def releases(self):
        """The releases property."""
        return self._releases

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    # =========================================================================
    #                         General methods
    # =========================================================================

    def _sort(self, attr):
        return sorted(attr, key=lambda x: x.key, reverse=False)

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def _reorder_nodes(self):
        '''Reorders the nodes to have consecutive keys. If the node label is an
        auto-generated label, it updates the label as well, otherwise leaves the
        user-generated label.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        k = 0
        for node in self.nodes:
            node.key = k
            k += 1
            if node.label[:2] == 'n-':
                node.label = 'n-{}'.format(node.key)

    def check_node_in_part(self, node):
        '''Checks if a node already exists in the Part in the same location.

        Parameters
        ----------
        node : obj
            compas_fea2 Node object.

        Returns
        -------
        indices : list
            List of the indices of all the instances of the node already in the
            Part.
        '''

        if node.gkey in self._nodes_gkeys:
            indices = [i for i, x in enumerate(self._nodes_gkeys) if x == node.gkey]
            return indices

    def add_node(self, node, check=True):
        """Add a compas_fea2 Node object to the Part. If the node object has
        no label, one is automatically assigned.

        Parameters
        ----------
        node : obj
            compas_fea2 Node object.
        check : bool
            If True, checks if the node is already present.

        Examples
        --------
        >>> part = Part('mypart')
        >>> node = Node(1.0, 2.0, 3.0)
        >>> part.add_node(node)
        """

        if check and self.check_node_in_part(node):
            print('WARNING: duplicate node at {} skipped!'.format(node.gkey))
        else:
            k = len(self.nodes)
            node._key = k
            if not node._name:
                node._name = 'n-{}'.format(k)
            self._nodes.append(node)
            self._nodes_gkeys.append(node.gkey)

    def add_nodes(self, nodes, check=True):
        """Add multiple compas_fea2 Node objects to the Part.

        Parameters
        ----------
        nodes : list
            List of compas_fea2 Node objects.
        check : bool
            If True, checks if the nodes are already present.

        Examples
        --------
        >>> part = Part('mypart')
        >>> node1 = Node(1.0, 2.0, 3.0)
        >>> node2 = Node(3.0, 4.0, 5.0)
        >>> part.add_nodes([node1, node2])
        """

        for node in nodes:
            self.add_node(node, check)

    def remove_node(self, node_key):
        '''Remove the node from the Part. If there are duplicate nodes, it
        removes also all the duplicates.

        Parameters
        ----------
        node_key : int
            Key number of the node to be removed.

        Returns
        -------
        None
        '''
        raise NotImplementedError()
        # del self.nodes[node_key]
        # del self.nodes_gkeys[node_key]
        # self._reorder_nodes()

    def remove_nodes(self, nodes):
        '''Remove the nodes from the Part. If there are duplicate nodes, it
        removes also all the duplicates.

        Parameters
        ----------
        node : list
            List with the key numbers of the nodes to be removed..

        Returns
        -------
        None
        '''
        raise NotImplementedError()
        # for node in nodes:
        #     self.remove_node(node)

    # =========================================================================
    #                           Elements methods
    # =========================================================================
    # def _check_element_in_part(self, element):
    #     """Check if the element is already in the model and in case add it.
    #     If `element` is of type `str`, check if the element is already defined.
    #     If `element` is of type `ElementBase`, add the element to the Part if not
    #     already defined.

    #     Warning
    #     -------
    #     the function does not check the elements connectivity. This could generate
    #     duplicate elements.

    #     Parameters
    #     ----------
    #     element : str or obj
    #         Name of the Part or Part object to check.

    #     Returns
    #     -------
    #     obj
    #         Part object

    #     Raises
    #     ------
    #     ValueError
    #         if `element` is a string and the element is not defined in the Part
    #     TypeError
    #         `element` must be either an instance of a `compas_fea2` Part class or the
    #         name of a Part already defined in the Problem.
    #     """
    #     if isinstance(element, str):
    #         if element not in self.elements:
    #             raise ValueError(f'{element} not found in the Part')
    #         element_name = element
    #     elif isinstance(element, PartBase):
    #         if element.name not in self.elements:
    #             self.add_element(element)
    #             print(f'{element.__repr__()} added to the Part')
    #         element_name = element.name
    #     else:
    #         raise TypeError(
    #             f'{element} is either not an instance of a `compas_fea2` ElementBase class or not found in the Model')

    #     return self.elements[element_name]

    def _reorder_elements(self):
        '''Reorders the elements to have consecutive keys.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        k = 0
        for element in self._elements:
            element.key = k
            k += 1

    def add_element(self, element):
        """Adds a compas_fea2 Element object to the Part.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.

        Returns
        -------
        None
        """

        element._key = len(self.elements)
        for c in element.connectivity:
            if c not in [node.key for node in self.nodes]:
                raise ValueError(
                    f'ERROR CREATING ELEMENT: node {c} not found. Check the connectivity indices of element: \n {element.__repr__()}!')
        self._elements[element._key] = element

        if isinstance(element.section, str):
            if element.section in self._sections:
                element._section = self._sections[element.section]
            else:
                raise ValueError(f'{element.section} not found in {self}')
        elif isinstance(element.section, SectionBase):
            self.add_section(element.section)
        else:
            raise ValueError('You must provide a Section object or the name of a previously added section')

    def add_elements(self, elements):
        """Adds multiple compas_fea2 Element objects to the Part.

        Parameters
        ----------
        elements : list
            List of compas_fea2 Element objects.
        check : bool
            If True, checks if the elements are already present.

        Returns
        -------
        None
        """

        for element in elements:
            self.add_element(element)

    def remove_element(self, element_key):
        '''Removes the element from the Part.

        Parameters
        ----------
        element_key : int
            Key number of the element to be removed.

        Returns
        -------
        None
        '''
        raise NotImplementedError()
        # # TODO check if element key exists
        # del self.elements[element_key]
        # self._reorder_elements()

    def remove_elements(self, elements):
        '''Removes the elements from the Part.

        Parameters
        ----------
        elements : list
            List with the key numbers of the element to be removed.

        Returns
        -------
        None
        '''
        raise NotImplementedError()

        # for element in elements:
        #     self.remove_element(element)

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    def add_release(self, release):
        self.releases.append(release)

    def add_releases(self, releases):
        for release in releases:
            self.add_release(release)

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        '''Add a Material object to the Part so that it can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            compas_fea2 material object.

        Returns
        -------
        None
        '''
        if material.name not in self._materials:
            self._materials[material.name] = material
        else:
            print('WARNING - {} already defined and it has been skipped! Note: the material name must be unique.')

    def add_materials(self, materials):
        '''Add multiple Material objects to the Part so that they can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : list
            List of compas_fea2 material objects.

        Returns
        -------
        None
        '''
        for material in materials:
            self.add_material(material)

    # =========================================================================
    #                        Sections methods
    # =========================================================================
    def add_section(self, section):
        """Add a compas_fea2 Section object to the Part.

        Parameters
        ----------
        section : obj
            compas_fea2 Section object.

        Returns
        -------
        None
        """
        if section.name not in self._sections:
            self._sections[section.name] = section
            if isinstance(section.material, MaterialBase):
                if section.material.name not in self._materials:
                    self.add_material(section.material)
            elif isinstance(section.material, str):
                if section.material in self._materials:
                    section._material = self._materials[section.material]
                else:
                    raise ValueError(f'Material {section.material} not found in {self}')
            else:
                raise ValueError()

    def add_sections(self, sections):
        """Add multiple compas_fea2 Section objects to the Part.

        Parameters
        ----------
        sections : list
            list of compas_fea2 Section objects.

        Returns
        -------
        None
        """
        for section in sections:
            self.add_section(section)

    # =========================================================================
    #                           Groups methods
    # =========================================================================
    def add_group(self, group):
        if isinstance(group, (NodesGroupBase, ElementsGroupBase)):
            if group.name not in self.groups:
                self._groups[group.name] = group
        else:
            raise ValueError('You must provide either a NodesGroup or an ElementsGroup object')

    def add_groups(self, groups):
        for group in groups:
            self.add_group(group)

    def add_nodes_group(self, name, nodes_keys):
        """Add a NodeGroup object to the the part .

        Parameters
        ----------
        name : str
            name of the group.
        nodes : list
            list of nodes keys to group
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.NodesGroup(name, nodes_keys)
        self._groups[name] = group

    def add_elements_group(self, name, elements_keys):
        """Add a ElementGroup object to the the part.

        Parameters
        ----------
        name : str
            name of the group.
        part : str
            name of the part
        elements : list
            list of elements keys to group
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.ElementsGroup(name, elements_keys)
        self._groups[name] = group

    def add_elements_to_group(self, group_name, element_keys):
        raise NotADirectoryError()

    def remove_element_group(self, group_name):
        raise NotImplementedError()

    def remove_element_from_group(self, group_name, element):
        raise NotImplementedError()
