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
    'Material',
    'Concrete',
    'ConcreteSmearedCrack',
    'ConcreteDamagedPlasticity',
    'ElasticIsotropic',
    'Stiff',
    'ElasticOrthotropic',
    'ElasticPlastic',
    # 'ThermalMaterial',
    'Steel',
    'UserMaterial'
]


class Material(MaterialBase):

    """ Initialises base Material object.

    Parameters
    ----------
    name : str
        Name of the Material object.

    Attributes
    ----------
    name : str
        Name of the Material object.

    """

    def __init__(self, name):
        super(Material, self).__init__(name, name)


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticIsotropic(ElasticIsotropicBase):

    """ Elastic, isotropic and homogeneous material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    tension : bool
        Can take tension.
    compression : bool
        Can take compression.

    """
    def __init__(self, name, E, v, p, tension, compression):
        super(ElasticIsotropic, self).__init__(name, E, v, p, tension, compression)

    def write_to_input_file(self, f):
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

    """ Elastic, very stiff and massless material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].

    """
    def __init__(self, name, E):
        super(Stiff, self).__init__(name, E)


class ElasticOrthotropic(ElasticOrthotropicBase):

    """ Elastic, orthotropic and homogeneous material.

    Parameters
    ----------
    name : str
        Material name.
    Ex : float
        Young's modulus Ex in x direction [Pa].
    Ey : float
        Young's modulus Ey in y direction [Pa].
    Ez : float
        Young's modulus Ez in z direction [Pa].
    vxy : float
        Poisson's ratio vxy in x-y directions [-].
    vyz : float
        Poisson's ratio vyz in y-z directions [-].
    vzx : float
        Poisson's ratio vzx in z-x directions [-].
    Gxy : float
        Shear modulus Gxy in x-y directions [Pa].
    Gyz : float
        Shear modulus Gyz in y-z directions [Pa].
    Gzx : float
        Shear modulus Gzx in z-x directions [Pa].
    p : float
        Density [kg/m3].
    tension : bool
        Can take tension.
    compression : bool
        Can take compression.

    Notes
    -----
    - Can be created but is currently not implemented.

    """
    pass
    # def __init__(self, name, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, p, tension, compression):
    #     super(ElasticOrthotropic, self).__init__(name, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, p, tension, compression)


# ==============================================================================
# non-linear general
# ==============================================================================

class ElasticPlastic(ElasticPlasticBase):

    """ Elastic and plastic, isotropic and homogeneous material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    f : list
        Plastic stress data (positive tension values) [Pa].
    e : list
        Plastic strain data (positive tension values) [-].

    Notes
    -----
    - Plastic stress--strain pairs applies to both compression and tension.

    """
    def __init__(self, name, E, v, p, f, e):
        super(ElasticPlastic, self).__init__(name, E, v, p, f, e)



# ==============================================================================
# non-linear metal
# ==============================================================================

class Steel(SteelBase):

    """ Bi-linear steel with given yield stress.

    Parameters
    ----------
    name : str
        Material name.
    fy : float
        Yield stress [MPa].
    fu : float
        Ultimate stress [MPa].
    eu : float
        Ultimate strain [%].
    E : float
        Young's modulus E [GPa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].

    """

    def __init__(self, name, fy, fu, eu, E, v, p):
        super(Steel, self).__init__(name, fy, fu, eu, E, v, p)



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

    """ Elastic and plastic-cracking Eurocode based concrete material.

    Parameters
    ----------
    name : str
        Material name.
    fck : float
        Characteristic (5%) 28 day cylinder strength [MPa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    fr : list
        Failure ratios.

    Notes
    -----
    - The concrete model is based on Eurocode 2 up to fck=90 MPa.

    """

    def __init__(self, name, fck, v, p, fr):
        super(Concrete, self).__init__(name, fck, v, p, fr)




class ConcreteSmearedCrack(ConcreteBaseSmearedCrack):

    """ Elastic and plastic, cracking concrete material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    fc : list
        Plastic stress data in compression [Pa].
    ec : list
        Plastic strain data in compression [-].
    ft : list
        Plastic stress data in tension [-].
    et : list
        Plastic strain data in tension [-].
    fr : list
        Failure ratios.

    """
    def __init__(self, name, E, v, p, fc, ec, ft, et, fr):
        super(ConcreteSmearedCrack, self).__init__(name, E, v, p, fc, ec, ft, et, fr)


class ConcreteDamagedPlasticity(ConcreteBaseDamagedPlasticity):

    """ Damaged plasticity isotropic and homogeneous material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    damage : list
        Damage parameters.
    hardening : list
        Compression hardening parameters.
    stiffening : list
        Tension stiffening parameters.

    """
    def __init__(self, name, E, v, p, damage, hardening, stiffening):
        super(ConcreteDamagedPlasticity, self).__init__(name, E, v, p, damage, hardening, stiffening)


# ==============================================================================
# thermal
# ==============================================================================

class ThermalMaterial(ThermalMaterialBase):

    """ Class for thermal material properties.

    Parameters
    ----------
    name : str
        Material name.
    conductivity : list
        Pairs of conductivity and temperature values.
    p : list
        Pairs of density and temperature values.
    sheat : list
        Pairs of specific heat and temperature values.

    """
    pass
    # def __init__(self, name, conductivity, p, sheat):
    #     super(ThermalMaterial, self).__init__(name, conductivity, p, sheat)


class UserMaterial(MaterialBase):

    """ User Defined Material (UMAT). Tho implement this type of material, a
    separate subroutine is required

    Parameters
    ----------
    name : str
        Material name.
    path : str
        Path to the subroutine (no spaces are allowed in the path!)
    **kwars : var
        constants needed for the UMAT definition (depends on the subroutine)
    """

    def __init__(self, name, path, p=None, **kwargs):
        MaterialBase.__init__(self, name=name)

        self.__name__    = 'UserMaterial'
        self.__dict__.update(kwargs)
        self.name        = name
        self.sub_path    = path #os.path.abspath(os.path.join(os.path.dirname(__file__), "umat/Umat_hooke_iso.f")) #TODO find a way to deal with space in windows command line
        self.p = p
        self.constants = self.get_constants()
        # self.attr_list.extend(['E', 'v', 'G', 'p', 'path'])

    def get_constants(self):
        constants = []
        for k in self.__dict__:
            if k not in ['__name__', 'name', 'attr_list', 'sub_path', 'p']:
                constants.append(self.__dict__[k])
        return constants


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
    material.to_input_file(f)
    f.close()
