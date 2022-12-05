from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.materials.concrete import Concrete
from compas_fea2.model.materials.concrete import ConcreteDamagedPlasticity
from compas_fea2.model.materials.concrete import ConcreteSmearedCrack

class SofistikConcrete(Concrete):
    """Sofistik implementation of :class:`compas_fea2.model.materials.concrete.Concrete`.\n
    """
    __doc__ += Concrete.__doc__

    def __init__(self, *, fck, v=0.2, density=2400, fr=None, name=None, **kwargs):
        super(SofistikConcrete, self).__init__(fck=fck, v=v, density=density, fr=fr, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikConcreteDamagedPlasticity(ConcreteDamagedPlasticity):
    """Sofistik implementation of :class:`compas_fea2.model.materials.concrete.ConcreteDamagedPlasticity`.\n
    """
    __doc__ += ConcreteDamagedPlasticity.__doc__

    def __init__(self, *, E, v, density, damage, hardening, stiffening, name=None, **kwargs):
        super(SofistikConcreteDamagedPlasticity, self).__init__(E=E, v=v, density=density, damage=damage, hardening=hardening, stiffening=stiffening, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikConcreteSmearedCrack(ConcreteSmearedCrack):
    """Sofistik implementation of :class:`compas_fea2.model.materials.concrete.ConcreteSmearedCrack`.\n
    """
    __doc__ += ConcreteSmearedCrack.__doc__

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], name=None, **kwargs):
        super(SofistikConcreteSmearedCrack, self).__init__(E=E, v=v, density=density, fc=fc, ec=ec, ft=ft, et=et, fr=fr, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

