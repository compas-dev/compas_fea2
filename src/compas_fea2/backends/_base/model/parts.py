from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import importlib

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.model.materials import MaterialBase
from compas_fea2.backends._base.model.sections import SectionBase

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

        self._nodes = []  # self._sort(nodes)
        self._nodes_gkeys = []

        self._materials = {}
        self._sections = {}

        self._elements = {}  # self._sort(elements)
        self._nsets = {}
        self._elsets = {}
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

    # @nodes.setter
    # def nodes(self, value):
    #     self._nodes = self.add_nodes(value)  # TODO complete this also for the other setters (tricky with dictionaries)

    @property
    def materials(self):
        """dict : Dictionary with the `Material` objects belonging to the Part."""
        return self._materials

    # @materials.setter
    # def materials(self, value):
    #     self._materials = value

    @property
    def sections(self):
        """dict : Dictionary with the `Section` objects belonging to the Part."""
        return self._sections

    # @sections.setter
    # def sections(self, value):
    #     self._sections = value

    @property
    def elements(self):
        """dict : Sorted list (by `Element key`) with the `Element` objects belonging to the Part."""
        return self._elements

    # @elements.setter
    # def elements(self, value):
    #     self._elements = value

    @property
    def nsets(self):
        """list : List with the `NodeSet` objects belonging to the `Part`."""
        return self._nsets

    # @nsets.setter
    # def nsets(self, value):
    #     self._nsets = value

    @property
    def elsets(self):
        """list : List with the `ElementSet` objects belonging to the `Part`."""
        return self._elsets

    # @elsets.setter
    # def elsets(self, value):
    #     self._elsets = value

    @property
    def releases(self):
        """The releases property."""
        return self._releases

    # @releases.setter
    # def releases(self, value):
    #     self._releases = value

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

    # def find_duplicate_nodes(self):
    #     '''Finds duplicate nodes in the Part.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     duplicates : dict
    #         Dictionary with the key numbers of the duplicate nodes
    #         keys: node geometric key
    #         values: node index
    #     '''

    #     duplicates = dict()
    #     for node in self.nodes:
    #         indices = self.check_node_in_part(node)
    #         if len(indices) >= 2:
    #             if not node.gkey in duplicates:
    #                 duplicates[node.gkey] = node.key
    #     return duplicates

    # def remove_duplicate_nodes(self):
    #     '''Removes duplicate nodes. Note that this alters the nodes indexing.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     None
    #     '''

    #     duplicates = self.find_duplicate_nodes()
    #     if duplicates:
    #         all_duplicates = []
    #         for key in duplicates.keys():
    #             for i in range(len(duplicates[key])-1):
    #                 all_duplicates.append(duplicates[key][i+1])

    #     for index in sorted(all_duplicates, reverse=True):
    #         del self._nodes[index]
    #         del self._nodes_gkeys[index]

    #     self._reorder_nodes()

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    def check_element_in_part(self, element):
        '''Checks if an element with the same connectivity already exists
        in the Part.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.

        Returns
        -------
        keys : list
            List with the key numbers of all the instances of the element already
            in the Part.
        '''
        # keys = []
        # for e in self._elements:
        #     if e.connectivity_key == element.connectivity_key:
        #         keys.append(e.key)
        # return keys
        return False

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

    def add_element(self, element, check=True):
        """Adds a compas_fea2 Element object to the Part.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.
        check : bool
            If True, checks if the element is already present.

        Returns
        -------
        None
        """

        if check and self.check_element_in_part(element):
            print('WARNING: duplicate element connecting {} skipped!'.format(element._connectivity_key))
        else:
            element._key = len(self.elements)
            for c in element._connectivity:
                if c not in [node._key for node in self.nodes]:
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

            # TODO review
            # # add the element key to its type group
            # if element.eltype not in self._elements_by_type.keys():
            #     self._elements_by_type[element.eltype] = []
            # self._elements_by_type[element.eltype].append(element.key)

            # # add the element key to its section group
            # if element.section not in self._elements_by_section.keys():
            #     self._elements_by_section[element.section] = []
            # self._elements_by_section[element.section].append(element.key)

            # # add the element orientation to its section group
            # if element.section not in self._orientations_by_section.keys():
            #     self._orientations_by_section[element.section] = []
            # if hasattr(element, 'orientation'):
            #     if element.orientation not in self._orientations_by_section[element.section]:
            #         self._orientations_by_section[element.section].append(element.orientation)
            # else:
            #     if None not in self._orientations_by_section[element.section]:
            #         self._orientations_by_section[element.section].append(None)
            # # else:
            # #     raise ValueError("ELEMENT ORIENTATION NOT DEFINED")

            # # # add the element key to its material group
            # # if element.section.material not in self.elements_by_material.keys():
            # #     self.elements_by_material[element.section.material] = []
            # # self.elements_by_material[element.section.material].append(element.key)
            # # add the element key to its elset group
            # if element.elset:
            #     #     element.elset = 'elset-{}'.format(len(self.elsets)) #element.section.name
            #     if element.elset not in self._elements_by_elset.keys():

            #         m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
            #         self.add_element_set(m.Set(element.elset, [], 'elset'))
            #         self._elements_by_elset[element.elset] = []
            #     self._elements_by_elset[element.elset].append(element.key)
            #     self.add_elements_to_set(element.elset, [element.key])

    def add_elements(self, elements, check=True):
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
            self.add_element(element, check)

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
        # else:
        #     print('WARNING: {} already added to the Part. skipped!')

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
    #                           Sets methods
    # =========================================================================
    def add_node_set(self, nset):
        raise NotImplementedError()

    def add_element_set(self, elset):
        if elset.name not in self._elsets:
            self._elsets[elset.name] = elset

    def add_elements_to_set(self, set_name, element_keys):
        raise NotADirectoryError()
        # for elset in self._elsets:
        #     if elset.name == set_name:
        #         for key in element_keys:
        #             if key not in elset.selection:
        #                 elset.selection.append(key)

    def remove_element_set(self, set_name):
        raise NotImplementedError()

    def remove_element_from_set(self, set_name, element):
        raise NotImplementedError()


# =============================================================================
#                               Debugging
# =============================================================================

if __name__ == "__main__":

    pass
