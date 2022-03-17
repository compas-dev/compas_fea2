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
    """OpenSees implementation of :class:`BeamElementBase`.\n
    """
    __doc__ += BeamElementBase.__doc__

    def __init__(self, connectivity, section, orientation=[0.0, 0.0, -1.0], thermal=None):
        super(BeamElement, self).__init__(connectivity, section, orientation, thermal)
        self._eltype = 'element elasticBeamColumn'

    def _generate_jobdata(self):
        line = []
        line.append('geomTransf Corotational {1}\n'.format(
            self.key, ' '.join([str(i) for i in self.orientation])))
        line.append('{} {} {} {} {} {} {} {} {} {} {}'.format(self._eltype,
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
