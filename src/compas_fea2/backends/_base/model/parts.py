from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'PartBase',
]

class PartBase():
    """Initialises a base Part object.

    Parameters
    ----------
    name : str
        Name of the set.

    Attributes
    ----------
    name : str
        Name of the set.
    nodes : list
        Sorted list (by Node key) with the Nodes objects belonging to the Part.
    nodes_gkeys : list
        List with the geometric keys (x_y_z) of the Nodes objects belonging to the Part.
    elements : list
        Sorted list (by Element key) with the Element objects belonging to the Part.
    nsets : list
        A list with the Set objects belonging to the Part.
    elsets : list
        [DOC]   # TODO: complete doc
    sections: dict
        [DOC]   # TODO: complete doc
    elements_by_type : dict
        Dictionary sorting the elements by unique element types.
        key: element type
        value: element key number
    elements_by_section : dict
        Dictionary sorting the elements by unique sections.
        key: section
        value: element key number
    elements_by_elset : dict
        Dictionary sorting the elements by their element set.
        key: elset
        value: element key number
    elements_by_material : dict
        Dictionary sorting the elements by unique materials.
        key: material
        value: element key number
    """

    def __init__(self, name):
        self.__name__                   = 'Part'
        self.name                       = name
        self.nodes                      = [] #self._sort(nodes)
        self.elements                   = [] #self._sort(elements)
        self.nsets                      = []
        self.elsets                     = []
        self.nodes_gkeys                = []
        self.sections                   = {}

        self.elements_by_type           = {}
        self.elements_by_section        = {}
        self.orientations_by_section    = {}
        self.elements_by_elset          = {}
        self.elsets_by_section          = {}
        # self.elements_by_material   = {}

    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        l = []
        for attr in ['name']:
            l.append('{0:<15} : {1}'.format(attr, getattr(self, attr)))
        l.append('{0:<15} : {1}'.format('# of nodes', len(self.nodes)))
        l.append('{0:<15} : {1}'.format('# of elements', len(self.elements)))
        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(l))

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
            node.key = k
            if not node.label:
                node.label = 'n-{}'.format(k)
            self.nodes.append(node)
            self.nodes_gkeys.append(node.gkey)

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

    # TODO remove methods need to be checked. For example, check if removing an element
    # also removes the sections and sets associated to it.

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

        del self.nodes[node_key]
        del self.nodes_gkeys[node_key]
        self._reorder_nodes()

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

        for node in nodes:
            self.remove_node(node)

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

        indices = []
        index = 0
        for gkey in self.nodes_gkeys:
            if gkey == node.gkey:
                indices.append(index)
            index +=1
        return indices

    def find_duplicate_nodes(self):
        '''Finds duplicate nodes in the Part.

        Parameters
        ----------
        None

        Returns
        -------
        duplicates : dict
            Dictionary with the key numbers of the duplicate nodes
            keys: node geometric key
            values: node index
        '''

        duplicates = dict()
        for node in self.nodes:
            indices = self.check_node_in_part(node)
            if len(indices)>=2:
                if not node.gkey in duplicates:
                    duplicates[node.gkey] = node.key
        return duplicates

    def remove_duplicate_nodes(self):
        '''Removes duplicate nodes. Note that this alters the nodes indexing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        duplicates = self.find_duplicate_nodes()
        if duplicates:
            all_duplicates = []
            for key in duplicates.keys():
                for i in range(len(duplicates[key])-1):
                    all_duplicates.append(duplicates[key][i+1])

        for index in sorted(all_duplicates, reverse=True):
            del self.nodes[index]
            del self.nodes_gkeys[index]

        self._reorder_nodes()

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

        keys = []
        for e in self.elements:
            if e.connectivity_key == element.connectivity_key:
                keys.append(e.key)
        return keys

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
        for element in self.elements:
            element.key = k
            k += 1
        self._group_elements()

    def _group_elements(self):
        '''Regenerates the elements groups.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        el_dict={}
        for el in self.elements:
            el_dict[el.key] = (el.eltype, el.section, el.elset, el.orientation)

        type_elements = {}
        section_elements = {}
        elset_elements = {}
        section_elsets = {}
        section_orientations = {}
        # material_elements = {}
        for key, value in el_dict.items():
            type_elements.setdefault(value[0], set()).add(key)
            section_elements.setdefault(value[1], set()).add(key)
            # material_elements.setdefault(value[1].material, set()).add(key)
            elset_elements.setdefault(value[2], set()).add(key)
            section_elsets.setdefault(value[1], set()).add(value[2])
            section_orientations.setdefault(value[1], set()).add(value[3])

        self.elements_by_type = type_elements
        self.elements_by_section = section_elements
        self.elements_by_elset = elset_elements
        self.orientations_by_section = section_orientations
        # self.elements_by_material = material_elements

        # self.remove_element_from_set()
        # for s in self.nsets:
        #     if not s:
        #         del self.nsets[s]

        # for s in self.elsets:
        #     if not s:
        #         del self.elsets[s]




    # =========================================================================
    #                           Sets methods
    # =========================================================================

    def add_element_set(self, elset):
        self.elsets.append(elset)

    def add_elements_to_set(self, set_name, element_keys):
        for elset in self.elsets:
            if elset.name == set_name:
                for key in element_keys:
                    if key not in elset.selection:
                        elset.selection.append(key)

    def remove_element_set(self, set_name):
        pass

    def remove_element_from_set(self, set_name, element):
        pass


# =============================================================================
#                               Debugging
# =============================================================================

if __name__ == "__main__":

    pass
