
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2._base.model import MaterialBase
from compas_fea2._base.model import ConcreteBase
from compas_fea2._base.model import ElasticIsotropicBase
from compas_fea2._base.model import StiffBase
from compas_fea2._base.model import ElasticOrthotropicBase
from compas_fea2._base.model import ElasticPlasticBase
from compas_fea2._base.model import SteelBase
from compas_fea2._base.model import ThermalMaterialBase


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticIsotropic(ElasticIsotropicBase):

    def __init__(self, name, E, v, p, unilateral=None):
        super(ElasticIsotropic, self).__init__(name, E, v, p)
        self.unilateral = unilateral
        # self._jobdata = self._generate_jobdata()

    def _generate_jobdata(self, m_index):
        line = []
        line.append('uniaxialMaterial Elastic {0} {1}\n'.format(m_index, self.E))
        line.append('nDMaterial ElasticIsotropic {0} {1} {2} {3}'.format(
            m_index + 1000, self.E, self.v, self.p))
        return ''.join(line)


### -------------------------------- DEBUG ------------------------------- ###
if __name__ == "__main__":

    material = ElasticIsotropic(name='test', E=10000, v=0.3, p=3000)
    print(material._generate_jobdata(1))
