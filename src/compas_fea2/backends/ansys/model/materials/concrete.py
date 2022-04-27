from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.materials.concrete import Concrete
from compas_fea2.model.materials.concrete import ConcreteDamagedPlasticity
from compas_fea2.model.materials.concrete import ConcreteSmearedCrack


class AnsysConcrete(Concrete):
    """ Ansys implementation of :class:`.Concrete`.\n
    """
    __doc__ += Concrete.__doc__

    def __init__(self, *, fck, v=0.2, density=2400, fr=None, name=None, **kwargs):
        super(AnsysConcrete, self).__init__(fck=fck, v=v, density=density, fr=fr, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysConcreteDamagedPlasticity(ConcreteDamagedPlasticity):
    """ Ansys implementation of :class:`.ConcreteDamagedPlasticity`.\n
    """
    __doc__ += ConcreteDamagedPlasticity.__doc__

    def __init__(self, *, E, v, density, damage, hardening, stiffening, name=None, **kwargs):
        super(AnsysConcreteDamagedPlasticity, self).__init__(E=E, v=v, density=density,
                                                             damage=damage, hardening=hardening, stiffening=stiffening, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysConcreteSmearedCrack(ConcreteSmearedCrack):
    """ Ansys implementation of :class:`.ConcreteSmearedCrack`.\n
    """
    __doc__ += ConcreteSmearedCrack.__doc__

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], name=None, **kwargs):
        super(AnsysConcreteSmearedCrack, self).__init__(E=E, v=v, density=density,
                                                        fc=fc, ec=ec, ft=ft, et=et, fr=fr, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
