
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import _Material
from compas_fea2.model import Concrete
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import Stiff
from compas_fea2.model import ElasticOrthotropic
from compas_fea2.model import ElasticPlastic
from compas_fea2.model import Steel


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticIsotropic(ElasticIsotropic):
    """OpenSees implementation of :class:`compas_fea2.model.materials.ElasticIsotropic`.\n
    """
    __doc__ += ElasticIsotropic.__doc__

    def __init__(self, name, E, v, p):
        super(ElasticIsotropic, self).__init__(name, E, v, p)

    def _generate_jobdata(self, m_index):
        line = [f'uniaxialMaterial Elastic {m_index} {self.E}\n',
                f'nDMaterial ElasticIsotropic {m_index + 1000} {self.E} {self.v} {self.p}']
        return ''.join(line)
