from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import Stiff
from compas_fea2.model import ElasticOrthotropic
from compas_fea2.model import ElasticPlastic
from compas_fea2.model import UserMaterial


# ==============================================================================
# linear elastic
# ==============================================================================

class OpenseesElasticOrthotropic(ElasticOrthotropic):
    """"""
    __doc__ += ElasticOrthotropic.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density, name=None, **kwargs):
        super(ElasticOrthotropic, self).__init__(Ex=Ex, Ey=Ey, Ez=Ez, vxy=vxy, vyz=vyz, vzx=vzx,
                                                 Gxy=Gxy, Gyz=Gyz, Gzx=Gzx, density=density, name=name, **kwargs)
        raise NotImplementedError


class OpenseesElasticIsotropic(ElasticIsotropic):
    """OpenSees implementation of :class:`compas_fea2.model.materials.ElasticIsotropic`.\n
    """
    __doc__ += ElasticIsotropic.__doc__

    def __init__(self, *, E, v, density, name=None, **kwargs):
        super(OpenseesElasticIsotropic, self).__init__(E=E, v=v, density=density, name=name, **kwargs)

    def _generate_jobdata(self, m_index):
        line = ['uniaxialMaterial Elastic {} {}\n'.format(m_index, self.E),
                'nDMaterial ElasticIsotropic {} {} {} {}'.format(m_index + 1000, self.E, self.v, self.density)]
        return ''.join(line)


class OpenseesStiff(Stiff):
    """"""
    __doc__ += Stiff.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesStiff, self).__init__(name, **kwargs)
        raise NotImplementedError

# ==============================================================================
# non-linear general
# ==============================================================================


class OpenseesElasticPlastic(ElasticPlastic):
    """"""
    __doc__ += ElasticPlastic.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, *, E, v, density, strain_stress, name=None, **kwargs):
        super(OpenseesElasticPlastic, self).__init__(E=E, v=v, density=density,
                                                     strain_stress=strain_stress, name=name, **kwargs)
        raise NotImplementedError


# ==============================================================================
# User-defined Materials
# ==============================================================================


class OpenseesUserMaterial(UserMaterial):
    """"""
    __doc__ += ElasticPlastic.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, name=None, **kwargs):
        super(OpenseesUserMaterial, self).__init__(self, name=name, **kwargs)
        raise NotImplementedError
