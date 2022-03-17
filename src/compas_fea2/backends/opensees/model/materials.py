
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2.model import MaterialBase
from compas_fea2.model import ConcreteBase
from compas_fea2.model import ElasticIsotropicBase
from compas_fea2.model import StiffBase
from compas_fea2.model import ElasticOrthotropicBase
from compas_fea2.model import ElasticPlasticBase
from compas_fea2.model import SteelBase
from compas_fea2.model import ThermalMaterialBase


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticIsotropic(ElasticIsotropicBase):
    """OpenSees implementation of :class:`ElasticIsotropicBase`.\n
    """
    __doc__ += ElasticIsotropicBase.__doc__

    def __init__(self, name, E, v, p):
        super(ElasticIsotropic, self).__init__(name, E, v, p)

    def _generate_jobdata(self, m_index):
        line = [f'uniaxialMaterial Elastic {m_index} {self.E}\n',
                f'nDMaterial ElasticIsotropic {m_index + 1000} {self.E} {self.v} {self.p}']
        return ''.join(line)
