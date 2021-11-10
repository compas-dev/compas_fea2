from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.model import NodeBase
from compas_fea2.backends._base.model import ElementBase
from compas_fea2.backends._base.model import MassElementBase
from compas_fea2.backends._base.model import BeamElementBase
from compas_fea2.backends._base.model import SpringElementBase
from compas_fea2.backends._base.model import TrussElementBase
from compas_fea2.backends._base.model import StrutElementBase
from compas_fea2.backends._base.model import TieElementBase
from compas_fea2.backends._base.model import ShellElementBase
from compas_fea2.backends._base.model import MembraneElementBase
# from compas_fea2.backends._base.model import FaceElementBase
from compas_fea2.backends._base.model import SolidElementBase
from compas_fea2.backends._base.model import PentahedronElementBase
from compas_fea2.backends._base.model import TetrahedronElementBase
from compas_fea2.backends._base.model import HexahedronElementBase


# Francesco Ranaudo (github.com/franaudo)

# TODO add the property class here

__all__ = [
    'BeamElement',
]


# ==============================================================================
# General
# ==============================================================================


# ==============================================================================
# 0D elements
# ==============================================================================


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(BeamElementBase):
    """A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self, connectivity, section, orientation=[0.0, 0.0, -1.0], elset=None, thermal=None):
        super(BeamElement, self).__init__(connectivity, section, thermal)
        self.elset = elset
        self.eltype = 'element elasticBeamColumn'
        self.orientation = orientation

    def _generate_data(self):
        line = []
        line.append('geomTransf Corotational {0} {1}\n'.format(
            self.eltype, ' '.join([str(i) for i in self.orientation])))
        line.append('{} {} {} {} {} {} {} {} {} {} {}'.format(self.eltype,
                                                              self.key,
                                                              self.connectivity[0],
                                                              self.connectivity[1],
                                                              self.section.A,
                                                              self.section.E,
                                                              self.section.G,
                                                              self.section.J,
                                                              self.section.Ixx,
                                                              self.section.Iyy,
                                                              self.key))
        return ''.join(line)


if __name__ == "__main__":
    from compas_fea2.backends.opensees.model.nodes import Node
    from compas_fea2.backends.opensees.model.materials import ElasticIsotropic
    from compas_fea2.backends.opensees.model.sections import SolidSection
    from compas_fea2.backends.opensees.model.elements import BeamElement

    nodes = [Node([i, 3, 4]) for i in range(4)]
    mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)
    sec = SolidSection(name='section_A', material='mat_A')
    print(sec._generate_data())
    b = BeamElement(connectivity=nodes, section=sec)

    print(b)
    print(b._generate_data())
