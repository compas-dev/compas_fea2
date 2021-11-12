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

    def _generate_jobdata(self):

        from compas_fea2.backends.abaqus.model import Set

        # Write nodes
        part_data = ['*Node\n']
        for node in self.nodes:
            part_data.append(node._generate_jobdata())

        # Write elements
        for eltype in self._elements_by_type:
            part_data.append("*Element, type={}\n".format(eltype))
            # data = []
            for key in self._elements_by_type[eltype]:
                part_data.append(self.elements[key]._generate_jobdata())

        # Write user-defined nsets
        for nset in self.nsets:
            part_data.append(nset._generate_jobdata())

        # Write sets
        for section in self._elements_by_section:
            # TODO this part is messy and needs to be rewritten
            # the main problem is that beam elements require orientations
            # while other elements (such shells) don't
            o = 1
            for orientation in self._orientations_by_section[section]:

                elements = []
                for element in self._elements_by_section[section]:
                    if hasattr(self._elements[element], 'orientation') and self.elements[element].orientation == orientation:
                        elements.append(element)
                    elif not hasattr(self.elements[element], 'orientation'):
                        elements.append(element)
                self.add_element_set(Set('_{}-{}'.format(section, o), elements, 'elset'))
                o += 1

        for elset in self.elsets:
            part_data.append(elset._generate_jobdata())

        # Write sections
        for section in self.sections.values():
            o = 1
            for orientation in self._orientations_by_section[section.name]:
                if orientation:
                    part_data.append(section._generate_jobdata('_{}-{}'.format(section.name, o), orientation))
                    o += 1
                else:
                    part_data.append(section._generate_jobdata('_{}-{}'.format(section.name, o)))

        # Write releases
        if self.releases:
            part_data.append('\n*Release\n')
            for release in self.releases:
                part_data.append(release._generate_jobdata())

        temp = ''.join(part_data)
        return ''.join(["*Part, name={}\n".format(self.name), temp,
                        "*End Part\n**\n"])


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
    print(part1._generate_jobdata())

    # nset = Set('test_neset', my_part.nodes)
    # my_part = Part(name='test', nodes=my_part.nodes, elements=[el_one, el_two, el_three, el_4], sets=[nset])

    # print(my_part.check_for_duplicate_nodes())

    # # print(type(my_part.elements_by_section[section_A]))
