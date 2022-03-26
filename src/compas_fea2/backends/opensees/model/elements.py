from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Node
from compas_fea2.model import _Element
from compas_fea2.model import MassElement
from compas_fea2.model import BeamElement
from compas_fea2.model import SpringElement
from compas_fea2.model import TrussElement
from compas_fea2.model import StrutElement
from compas_fea2.model import TieElement
from compas_fea2.model import ShellElement
from compas_fea2.model import MembraneElement
# from compas_fea2.model import FaceElement
from compas_fea2.model import SolidElement
from compas_fea2.model import PentahedronElement
from compas_fea2.model import TetrahedronElement
from compas_fea2.model import HexahedronElement


# ==============================================================================
# General
# ==============================================================================


# ==============================================================================
# 0D elements
# ==============================================================================


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(BeamElement):
    """OpenSees implementation of :class:`compas_fea2.model.BeamElement`.\n
    """
    __doc__ += BeamElement.__doc__

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
