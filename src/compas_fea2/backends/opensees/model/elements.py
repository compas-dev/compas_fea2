from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import NodeBase
from compas_fea2.model import ElementBase
from compas_fea2.model import MassElementBase
from compas_fea2.model import BeamElementBase
from compas_fea2.model import SpringElementBase
from compas_fea2.model import TrussElementBase
from compas_fea2.model import StrutElementBase
from compas_fea2.model import TieElementBase
from compas_fea2.model import ShellElementBase
from compas_fea2.model import MembraneElementBase
# from compas_fea2.model import FaceElementBase
from compas_fea2.model import SolidElementBase
from compas_fea2.model import PentahedronElementBase
from compas_fea2.model import TetrahedronElementBase
from compas_fea2.model import HexahedronElementBase


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

    def _generate_jobdata(self):
        line = []
        line.append('geomTransf Corotational {1}\n'.format(
            self.key, ' '.join([str(i) for i in self.orientation])))
        line.append('{} {} {} {} {} {} {} {} {} {} {}'.format(self.eltype,
                                                              self.key,
                                                              self.connectivity[0],
                                                              self.connectivity[1],
                                                              self.section.A,
                                                              self.section.material.E,
                                                              self.section.material.G,
                                                              self.section.J,
                                                              self.section.Ixx,
                                                              self.section.Iyy,
                                                              self.key))
        return ''.join(line)


if __name__ == "__main__":
    pass
