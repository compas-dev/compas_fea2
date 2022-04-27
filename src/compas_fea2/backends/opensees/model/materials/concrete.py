from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Concrete
from compas_fea2.model import ConcreteSmearedCrack
from compas_fea2.model import ConcreteDamagedPlasticity

# ==============================================================================
# non-linear concrete
# ==============================================================================


class OpenseesConcrete(Concrete):
    """"""
    __doc__ += Concrete.__doc__

    def __init__(self, *, fck, v=0.2, density=2400, fr=None,  name=None, **kwargs):
        super(OpenseesConcrete, self).__init__(fck=fck, v=v, density=density, fr=fr, name=name, **kwargs)
        raise NotImplementedError


class OpenseesConcreteSmearedCrack(ConcreteSmearedCrack):
    """"""
    __doc__ += ConcreteSmearedCrack.__doc__

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], name=None, **kwargs):
        super(OpenseesConcreteSmearedCrack, self).__init__(E=E, v=v, density=density,
                                                           fc=fc, ec=ec, ft=ft, et=et, fr=fr, name=name, **kwargs)
        raise NotImplementedError


class OpenseesConcreteDamagedPlasticity(ConcreteDamagedPlasticity):
    """"""
    __doc__ += ConcreteDamagedPlasticity.__doc__

    def __init__(self, *, E, v, density, damage, hardening, stiffening, name=None, **kwargs):
        super(OpenseesConcreteDamagedPlasticity, self).__init__(E=E, v=v,
                                                                density=density, damage=damage, hardening=hardening, stiffening=stiffening, name=name, **kwargs)
        raise NotImplementedError
