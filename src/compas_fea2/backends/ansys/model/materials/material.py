from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.materials.material import ElasticIsotropic
from compas_fea2.model.materials.material import ElasticOrthotropic
from compas_fea2.model.materials.material import ElasticPlastic
from compas_fea2.model.materials.material import Stiff
from compas_fea2.model.materials.material import UserMaterial

class AnsysElasticIsotropic(ElasticIsotropic):
    """ Ansys implementation of :class:`.ElasticIsotropic`.\n
    """
    __doc__ += ElasticIsotropic.__doc__

    def __init__(self, *, E, v, density, name=None, **kwargs):
        super(AnsysElasticIsotropic, self).__init__(E=E, v=v, density=density, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysElasticOrthotropic(ElasticOrthotropic):
    """ Ansys implementation of :class:`.ElasticOrthotropic`.\n
    """
    __doc__ += ElasticOrthotropic.__doc__

    def __init__(self, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density, name=None, **kwargs):
        super(AnsysElasticOrthotropic, self).__init__(Ex=Ex, Ey=Ey, Ez=Ez, vxy=vxy, vyz=vyz, vzx=vzx, Gxy=Gxy, Gyz=Gyz, Gzx=Gzx, density=density, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysElasticPlastic(ElasticPlastic):
    """ Ansys implementation of :class:`.ElasticPlastic`.\n
    """
    __doc__ += ElasticPlastic.__doc__

    def __init__(self, *, E, v, density, strain_stress, name=None, **kwargs):
        super(AnsysElasticPlastic, self).__init__(E=E, v=v, density=density, strain_stress=strain_stress, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysStiff(Stiff):
    """ Ansys implementation of :class:`.Stiff`.\n
    """
    __doc__ += Stiff.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysStiff, self).__init__(name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysUserMaterial(UserMaterial):
    """ Ansys implementation of :class:`.UserMaterial`.\n
    """
    __doc__ += UserMaterial.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysUserMaterial, self).__init__(name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

