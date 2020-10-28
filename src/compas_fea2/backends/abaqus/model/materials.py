from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import log
import os

from compas_fea2.backends._base.model import MaterialBase
from compas_fea2.backends._base.model import ConcreteBase
from compas_fea2.backends._base.model import ConcreteSmearedCrackBase
from compas_fea2.backends._base.model import ConcreteDamagedPlasticityBase
from compas_fea2.backends._base.model import ElasticIsotropicBase
from compas_fea2.backends._base.model import StiffBase
from compas_fea2.backends._base.model import ElasticOrthotropicBase
from compas_fea2.backends._base.model import ElasticPlasticBase
from compas_fea2.backends._base.model import SteelBase
from compas_fea2.backends._base.model import ThermalMaterialBase


# Author(s): Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'ElasticIsotropic',
    'Stiff',
    'ElasticOrthotropic',
    'ElasticPlastic',
    # 'ThermalMaterial',
    'Steel',
    'Concrete',
    'ConcreteSmearedCrack',
    'ConcreteDamagedPlasticity',
    'UserMaterial'
]



# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticIsotropic(ElasticIsotropicBase):

    def __init__(self, name, E, v, p, unilateral=None):
        super(ElasticIsotropic, self).__init__(name, E, v, p)
        self.unilateral = unilateral
        self.data = self._generate_data()

    def _generate_data(self):
        n=''
        if self.unilateral:
            if self.unilateral == 'nc':
                n = '\n*NO COMPRESSION'
            elif self.unilateral == 'nt':
                n = '\n*NO TENSION'
            else:
                raise Exception('keyword {} for unilateral parameter not recognised. Please review the documentation'.format(self.unilateral))

        return ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}{}\n").format(self.name, self.p, self.E['E'], self.v['v'], n)


class Stiff(StiffBase):

    def __init__(self, name, E):
        super(Stiff, self).__init__(name, E)
        self.data = self._generate_data()

    def _generate_data(self):
        return ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n").format(self.name, self.p, self.E['E'], self.v['v'])


class ElasticOrthotropic(ElasticOrthotropicBase):
    NotImplemented


# ==============================================================================
# non-linear general
# ==============================================================================

class ElasticPlastic(ElasticPlasticBase):

    def __init__(self, name, E, v, p, f, e):
        super(ElasticPlastic, self).__init__(name, E, v, p, f, e)
        self.data = self._generate_data()

    def _generate_data(self):
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Plastic").format(self.name, self.p, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)
        return '\n'.join(data_section)


# ==============================================================================
# non-linear metal
# ==============================================================================

class Steel(SteelBase):

    def __init__(self, name, fy, fu, eu, E, v, p):
        super(Steel, self).__init__(name, fy, fu, eu, E, v, p)
        self.data = self._generate_data()

    def _generate_data(self):
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Plastic").format(self.name, self.p, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)
        return '\n'.join(data_section)

# ==============================================================================
# non-linear timber
# ==============================================================================


# ==============================================================================
# non-linear masonry
# ==============================================================================


# ==============================================================================
# non-linear concrete
# ==============================================================================

class Concrete(ConcreteBase):

    def __init__(self, name, fck, v, p, fr):
        super(Concrete, self).__init__(name, fck, v, p, fr)
        self.data = self._generate_data()

    def _generate_data(self):
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Concrete\n").format(self.name, self.p, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)

            data_section.append('*Tension stiffening')

        for i, j in zip(self.tension['f'], self.tension['e']):
            line = """{}, {}""".format(i, j)
            data_section.append(line)

        a, b = self.fratios
        line = ("*Failure ratios\n"
                "{}, {}").format(a, b)
        data_section.append(line)
        return '\n'.join(data_section)


class ConcreteSmearedCrack(ConcreteSmearedCrackBase):

    def __init__(self, name, E, v, p, fc, ec, ft, et, fr):
        super(ConcreteSmearedCrack, self).__init__(name, E, v, p, fc, ec, ft, et, fr)
        self.data = self._generate_data()

    def _generate_data(self):
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Concrete\n").format(self.name, self.p, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)

            data_section.append('*Tension stiffening')

        for i, j in zip(self.tension['f'], self.tension['e']):
            line = """{}, {}""".format(i, j)
            data_section.append(line)

        a, b = self.fratios
        line = ("*Failure ratios\n"
                "{}, {}").format(a, b)
        data_section.append(line)
        return '\n'.join(data_section)

class ConcreteDamagedPlasticity(ConcreteDamagedPlasticityBase):

    def __init__(self, name, E, v, p, damage, hardening, stiffening):
        super(ConcreteDamagedPlasticity, self).__init__(name, E, v, p, damage, hardening, stiffening)
        self.data = self._generate_data()

    def _generate_data(self):
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Concrete Damaged Plasticity\n").format(self.name, self.p, self.E['E'], self.v['v'])
        data_section.append(line)

        data_section.append(', '.join([str(i) for i in self.damage]))
        data_section.append('*CONCRETE COMPRESSION HARDENING')
        for i in self.hardening:
            data_section.append(', '.join([str(j) for j in i]))

        data_section.append('*Concrete Tension Stiffening, type=GFI')
        for i in self.stiffening:
            data_section.append(', '.join([str(j) for j in i]))

        return '\n'.join(data_section)

# ==============================================================================
# thermal
# ==============================================================================

class ThermalMaterial(ThermalMaterialBase):
    NotImplemented


class UserMaterial(MaterialBase):

    """ User Defined Material (UMAT). Tho implement this type of material, a
    separate subroutine is required

    Parameters
    ----------
    name : str
        Material name.
    sub_path : str
        Path to the subroutine (no spaces are allowed in the path!)
    **kwars : var
        constants needed for the UMAT definition (depends on the subroutine)
    """

    def __init__(self, name, sub_path, p=None, **kwargs):
        MaterialBase.__init__(self, name=name)

        self.__name__    = 'UserMaterial'
        self.__dict__.update(kwargs)
        self.name        = name
        self.sub_path    = sub_path #os.path.abspath(os.path.join(os.path.dirname(__file__), "umat/Umat_hooke_iso.f")) #TODO find a way to deal with space in windows command line
        self.p           = p
        self.constants = self.get_constants()
        # self.attr_list.extend(['E', 'v', 'G', 'p', 'path'])

        self.data = self._generate_data()

    def get_constants(self):
        constants = []
        for k in self.__dict__:
            # TODO: I think we should we add constants in the list below?
            if k not in ['__name__', 'name', 'attr_list', 'sub_path', 'p']:
                constants.append(self.__dict__[k])
        return constants

    def _generate_data(self):
        k = [str(i) for i in self.constants]
        return ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*User Material, constants={}\n"
                "{}").format(self.name, self.p, len(k), ', '.join(reversed(k)))


### -------------------------------- DEBUG ------------------------------- ###


if __name__ == "__main__":

    material = ElasticIsotropic(name='test', E=1, v=2, p=3)
    plastic = ElasticPlastic('plastic', 1,2,3,[4,5],[6,7])
    umat = UserMaterial(name='my_umat', sub_path='C:/', p=10, v=30, E=20)
    print(umat.data)
