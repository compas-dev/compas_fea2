from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from compas_fea2.model import PartBase


class Part(PartBase):
    """OpenSees implementation of :class:`PartBase`.\n
    """
    __doc__ += PartBase.__doc__

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
    from compas_fea2.backends.opensees import ElasticIsotropic
    from compas_fea2.backends.opensees import RectangularSection
    from compas_fea2.backends.opensees import BeamElement

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
    section_A = RectangularSection(name='section_A', b=10, h=20, material=mat1)

    # Generate elements between nodes
    elements = []
    for e in range(len(part1.nodes)-1):
        elements.append((BeamElement([e, e+1], section_A)))
    part1.add_elements(elements)
    part1.add_element(BeamElement([29, 0], section_A))
    print(part1)
