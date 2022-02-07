from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from compas_fea2.model import PartBase

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
    """

    def __init__(self, name):
        super(Part, self).__init__(name)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def _generate_jobdata(self):
        pass


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":

    from compas_fea2.backends.opensees import Node
    from compas_fea2.backends.opensees import Concrete
    from compas_fea2.backends.opensees import ElasticIsotropic
    from compas_fea2.backends.opensees import BoxSection
    from compas_fea2.backends.opensees import SolidSection
    from compas_fea2.backends.opensees import BeamElement
    from compas_fea2.backends.opensees import SolidElement
    from compas_fea2.backends.opensees import Set

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
