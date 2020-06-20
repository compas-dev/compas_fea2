from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import log
import os

# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2.backends._core import MaterialBase
from compas_fea2.backends._core import ConcreteBase
from compas_fea2.backends._core import ConcreteBaseSmearedCrack
from compas_fea2.backends._core import ConcreteBaseDamagedPlasticity
from compas_fea2.backends._core import ElasticIsotropicBase
from compas_fea2.backends._core import StiffBase
from compas_fea2.backends._core import ElasticOrthotropicBase
from compas_fea2.backends._core import ElasticPlasticBase
from compas_fea2.backends._core import SteelBase
from compas_fea2.backends._core import ThermalMaterialBase


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

    def __init__(self, name, E, v, p, tension=None, compression=None):
        super(ElasticIsotropic, self).__init__(name, E, v, p, tension, compression)

    def write_data(self, f):
        no_c=''
        no_t=''
        if not self.compression:
            no_c = '\n*NO COMPRESSION'
        if not self.tension:
            no_t = '\n*NO TENSION'

        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}{}{}
""".format(self.name, self.p, self.E['E'], self.v['v'], no_c, no_t)

        f.write(line)

class Stiff(StiffBase):

    def __init__(self, name, E):
        super(Stiff, self).__init__(name, E)

    def write_data(self, f):
        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}
""".format(self.name, self.p, self.E['E'], self.v['v'])
        f.write(line)

class ElasticOrthotropic(ElasticOrthotropicBase):
    NotImplemented
    pass


# ==============================================================================
# non-linear general
# ==============================================================================

class ElasticPlastic(ElasticPlasticBase):

    def __init__(self, name, E, v, p, f, e):
        super(ElasticPlastic, self).__init__(name, E, v, p, f, e)

    def write_data(self, f):
        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}
*Plastic
""".format(self.name, self.p, self.E['E'], self.v['v'])
        f.write(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            f.write(line)


# ==============================================================================
# non-linear metal
# ==============================================================================

class Steel(SteelBase):

    def __init__(self, name, fy, fu, eu, E, v, p):
        super(Steel, self).__init__(name, fy, fu, eu, E, v, p)

    def write_data(self, f):
        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}
*Plastic
""".format(self.name, self.p, self.E['E'], self.v['v'])
        f.write(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            f.write(line)


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

    def write_data(self, f):
        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}
*Concrete
""".format(self.name, self.p, self.E['E'], self.v['v'])
        f.write(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            f.write(line)

        f.write('*Tension stiffening')

        for i, j in zip(self.tension['f'], self.tension['e']):
            line = """{}, {}""".format(i, j)
            f.write(line)

        a, b = self.fratios
        line = """*Failure ratios
{}, {}""".format(a, b)
        f.write(line)
class ConcreteSmearedCrack(ConcreteBaseSmearedCrack):

    def __init__(self, name, E, v, p, fc, ec, ft, et, fr):
        super(ConcreteSmearedCrack, self).__init__(name, E, v, p, fc, ec, ft, et, fr)

    def write_data(self, f):
        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}
*Concrete
""".format(self.name, self.p, self.E['E'], self.v['v'])
        f.write(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            f.write(line)

        f.write('*Tension stiffening')

        for i, j in zip(self.tension['f'], self.tension['e']):
            line = """{}, {}""".format(i, j)
            f.write(line)

        a, b = self.fratios
        line = """*Failure ratios
{}, {}""".format(a, b)
        f.write(line)

class ConcreteDamagedPlasticity(ConcreteBaseDamagedPlasticity):

    def __init__(self, name, E, v, p, damage, hardening, stiffening):
        super(ConcreteDamagedPlasticity, self).__init__(name, E, v, p, damage, hardening, stiffening)

    def write_data(self, f):
        line = """*Material, name={}
*Density
{},
*Elastic
{}, {}
*Concrete Damaged Plasticity
""".format(self.name, self.p, self.E['E'], self.v['v'])
        f.write(line)

        f.write(', '.join([str(i) for i in self.damage]))
        f.write('*CONCRETE COMPRESSION HARDENING')
        for i in self.hardening:
            f.write(', '.join([str(j) for j in i]))


        f.write('*Concrete Tension Stiffening, type=GFI')
        for i in self.stiffening:
            f.write(', '.join([str(j) for j in i]))


# ==============================================================================
# thermal
# ==============================================================================

class ThermalMaterial(ThermalMaterialBase):
    NotImplemented
    pass


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

    def get_constants(self):
        constants = []
        for k in self.__dict__:
            if k not in ['__name__', 'name', 'attr_list', 'sub_path', 'p']:
                constants.append(self.__dict__[k])
        return constants

    def write_data(self, f):
        k = [str(i) for i in self.constants]
        line = """*Material, name={}
*Density
{},
*User Material, constants={}
{}""".format(self.name, self.p, len(k), ', '.join(reversed(k)))  #TODO check it reversed or not
        f.write(line)


### -------------------------------- DEBUG ------------------------------- ###

if __name__ == "__main__":
    # umat = UserMaterial(name='umat', path='test/path.f', p=30, E=10, v=1000)
    # k=[str(i) for i in umat.constants]
    # print(k)
    # print(', '.join(k))
    def write_to_file(my_string, destination_path):
        f=open(destination_path,'w')
        f.write(my_string)
        f.close()

    # material = ElasticIsotropic(name='test', E=1, v=2, p=3, tension=False, compression=True)
    # print(material.to_input_file())
    # write_to_file(material.to_input_file(), 'C:/temp/test_input.inp')
    f=open('C:/temp/test_input.inp','w')
    material = ElasticIsotropic(name='test', E=1, v=2, p=3, tension=False, compression=True)
    umat = UserMaterial(name='my_umat', sub_path='C;/', p=10, v=30, E=20)
    umat.write_data(f)
    f.close()
