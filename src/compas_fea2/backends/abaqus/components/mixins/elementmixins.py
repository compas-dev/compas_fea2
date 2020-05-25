
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._core.components.mixins import ElementMixinsBase

from compas_fea2.backends.abaqus.components.elements import *


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'ElementMixins',
]


func_dict = {
    'BeamElement':        BeamElement,
    'SpringElement':      SpringElement,
    'TrussElement':       TrussElement,
    'StrutElement':       StrutElement,
    'TieElement':         TieElement,
    'ShellElement':       ShellElement,
    'MembraneElement':    MembraneElement,
    'FaceElement':        FaceElement,
    'SolidElement':       SolidElement,
    'TetrahedronElement': TetrahedronElement,
    'PentahedronElement': PentahedronElement,
    'HexahedronElement':  HexahedronElement,
    'MassElement':        MassElement
}


class ElementMixins(ElementMixinsBase):

    def __init__(self):
        super(ElementMixins, self).__init__()


    def add_nodal_element(self, node, type, virtual_node=False):

        """ Adds a nodal element to structure.elements with the possibility of
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
        - Elements are numbered sequentially starting from 0.

        """

        if virtual_node:
            xyz = self.node_xyz(node)
            key = self.virtual_nodes.setdefault(node, self.node_count())
            self.nodes[key] = {'x': xyz[0], 'y': xyz[1], 'z': xyz[2],
                               'ex': [1, 0, 0], 'ey': [0, 1, 0], 'ez': [0, 0, 1], 'virtual': True}
            if 'virtual_nodes' in self.sets:
                self.sets['virtual_nodes']['selection'].append(key)
            else:
                self.sets['virtual_nodes'] = {'type': 'node', 'selection': [key], 'explode': False}
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

        """ Adds a virtual element to structure.elements and to element set 'virtual_elements'.

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
        - Virtual elements are numbered sequentially starting from 0.

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
                self.sets['virtual_elements']['selection'].append(ekey)
            else:
                self.sets['virtual_elements'] = {'type': 'virtual_element', 'selection': [ekey],
                                                 'index': len(self.sets)}

        return ekey


    def assign_element_property(self, element_property):

        """ Assign the ElementProperties object name to associated Elements.

        Parameters
        ----------
        element_property : obj
            ElementProperties object.

        Returns
        -------
        None

        """

        if element_property.elset:
            elements = self.sets[element_property.elset].selection
        else:
            elements = element_property.elements

        for element in elements:
            self.elements[element].element_property = element_property.name
