from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from compas_fea2.backends._base.model import PartBase

# from compas_fea2.backends.abaqus.components import Node


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Part',
]

class Part(PartBase):
    """Initialises a Part object.

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
        super(Part, self).__init__(name)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def _generate_data(self):

        from compas_fea2.backends.abaqus.model import Set

        # Write nodes
        part_data = ['*Node\n']
        for node in self.nodes:
            part_data.append(node._generate_data())

        # Write elements
        for eltype in self.elements_by_type:
            part_data.append("*Element, type={}\n".format(eltype))
            # data = []
            for key in self.elements_by_type[eltype]:
                part_data.append(self.elements[key]._generate_data())

        # Write user-defined nsets
        for nset in self.nsets:
            part_data.append(nset._generate_data())

        # Write sets
        for section in self.elements_by_section:
            #TODO this part is messy and needs to be rewritten
            # the main problem is that beam elements require orientations
            # while other elements (such shells) don't
            o=1
            for orientation in self.orientations_by_section[section]:

                elements = []
                for element in self.elements_by_section[section]:
                    if hasattr(self.elements[element], 'orientation') and self.elements[element].orientation == orientation:
                        elements.append(element)
                    elif not hasattr(self.elements[element], 'orientation'):
                        elements.append(element)
                self.add_element_set(Set('_{}-{}'.format(section, o), elements, 'elset'))
                o+=1

        for elset in self.elsets:
            part_data.append(elset._generate_data())

        # Write sections
        for section in self.sections.values():
            o=1
            for orientation in self.orientations_by_section[section.name]:
                if orientation:
                    part_data.append(section._generate_data('_{}-{}'.format(section.name, o), orientation))
                    o+=1
                else:
                    part_data.append(section._generate_data('_{}-{}'.format(section.name, o)))

        temp = ''.join(part_data)
        return ''.join(["*Part, name={}\n".format(self.name), temp,
                        "*End Part\n**\n"])




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
            print('WARNING: duplicate element connecting {} skipped!'.format(element.connectivity_key))
        else:
            for c in element.connectivity:
                if c > len(self.nodes)-1:
                    sys.exit('ERROR CREATING ELEMENT: node {} not found. Check the connectivity indices of element: \n {}!'.format(c, element))
            element.key = len(self.elements)
            self.elements.append(element)

            # add the element key to its type group
            if element.eltype not in self.elements_by_type.keys():
                self.elements_by_type[element.eltype] = []
            self.elements_by_type[element.eltype].append(element.key)

            # add the element key to its section group
            if element.section not in self.elements_by_section.keys():
                self.elements_by_section[element.section] = []
            self.elements_by_section[element.section].append(element.key)

            # add the element orientation to its section group
            if element.section not in self.orientations_by_section.keys():
                self.orientations_by_section[element.section] = []
            if hasattr(element, 'orientation'):
                if element.orientation not in self.orientations_by_section[element.section]:
                    self.orientations_by_section[element.section].append(element.orientation)


            else:
                if None not in self.orientations_by_section[element.section]:
                    self.orientations_by_section[element.section].append(None)
            # else:
            #     raise ValueError("ELEMENT ORIENTATION NOT DEFINED")
            #     # sys.exit("ELEMENT ORIENTATION NOT DEFINED")



            # # add the element key to its material group
            # if element.section.material not in self.elements_by_material.keys():
            #     self.elements_by_material[element.section.material] = []
            # self.elements_by_material[element.section.material].append(element.key)

            # add the element key to its elset group
            if element.elset:
            #     element.elset = 'elset-{}'.format(len(self.elsets)) #element.section.name
                if element.elset not in self.elements_by_elset.keys():
                    import importlib

                    mymodule = importlib.import_module('matplotlib.text')
                    from compas_fea2.backends.abaqus.model import Set
                    self.add_element_set(Set(element.elset, [], 'elset'))
                    self.elements_by_elset[element.elset] = []
                self.elements_by_elset[element.elset].append(element.key)
                self.add_elements_to_set(element.elset, [element.key])

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
        #TODO check if element key exists
        del self.elements[element_key]
        self._reorder_elements()

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

        for element in elements:
            self.remove_node(element)

# =============================================================================
#                               Debugging
# =============================================================================

if __name__ == "__main__":

    from compas_fea2.backends.abaqus import Node
    from compas_fea2.backends.abaqus import Concrete
    from compas_fea2.backends.abaqus import ElasticIsotropic
    from compas_fea2.backends.abaqus import BoxSection
    from compas_fea2.backends.abaqus import SolidSection
    from compas_fea2.backends.abaqus import BeamElement
    from compas_fea2.backends.abaqus import SolidElement
    from compas_fea2.backends.abaqus import Set

    part1 = Part(name='part-1')

    # Add nodes to the part
    for x in range(0, 1100, 100):
        part1.add_node(Node([x, 0.0, 0.0]))
    for y in range(100, 600, 100):
        part1.add_node(Node([x, y, 0.0]))
    for x in range(900, -100, -100):
        part1.add_node(Node([x, y, 0.0]))
    for y in range(400, 0, -100):
        part1.add_node(Node([x, y, 0.0]))


    # Define materials
    mat1 = ElasticIsotropic(name='mat1', E=29000, v=0.17, p=2.5e-9)
    mat2 = ElasticIsotropic(name='mat2', E=25000, v=0.17, p=2.4e-9)

    # Define sections
    section_A = SolidSection(name='section_A', material=mat1)
    section_B = BoxSection(name='section_B', material=mat2, a=50, b=100, t1=5, t2=5, t3=5, t4=5)

    # Generate elements between nodes
    elements = []
    for e in range(len(part1.nodes)-1):
        elements.append((BeamElement([e, e+1], section_B)))
    part1.add_elements(elements)
    part1.add_element(BeamElement([29, 0], section_A, elset='test'))
    print(part1.elements_by_type)
    print(part1._generate_data())

    # nset = Set('test_neset', my_part.nodes)
    # my_part = Part(name='test', nodes=my_part.nodes, elements=[el_one, el_two, el_three, el_4], sets=[nset])

    # print(my_part.check_for_duplicate_nodes())

    # # print(type(my_part.elements_by_section[section_A]))

