from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import log

from compas_fea2._base.base import FEABase

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


# TODO: make units independent
# TODO: remove att_list attribute

__all__ = [
    'MaterialBase',
    'ConcreteBase',
    'ConcreteSmearedCrackBase',
    'ConcreteDamagedPlasticityBase',
    'ElasticIsotropicBase',
    'StiffBase',
    'ElasticOrthotropicBase',
    'ElasticPlasticBase',
    'ThermalMaterialBase',
    'SteelBase'
]


class MaterialBase(FEABase):
    """Initialises base Material object.

    Parameters
    ----------
    name : str
        Name of the Material object.
    """

    def __init__(self, name):
        self.__name__ = 'Material'
        self._name = name

    @property
    def name(self):
        """str : Name of the Material object."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticOrthotropicBase(MaterialBase):
    """Elastic, orthotropic and homogeneous material.

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

    Warnings
    --------
    Can be created but is currently not implemented.
    """

    def __init__(self, name, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, p):
        super(ElasticOrthotropicBase, self).__init__(name=name)
        self.__name__ = 'ElasticOrthotropic'
        self._Ex = Ex
        self._Ey = Ey
        self._Ez = Ez
        self._vxy = vxy
        self._vyz = vyz
        self._vzx = vzx
        self._Gxy = Gxy
        self._Gyz = Gyz
        self._Gzx = Gzx
        self._p = p

    @property
    def Ex(self):
        """float : Young's modulus E along X, for example [Pa]."""
        return self._Ex

    @property
    def Ey(self):
        """float : Young's modulus E along Y, for example [Pa]."""
        return self._Ey

    @property
    def Ez(self):
        """float : Young's modulus E along Z, for example [Pa]."""
        return self._Ez

    @property
    def vxy(self):
        """float : Poisson's ratio vxy in x-y directions [unitless]."""
        return self._vxy

    @property
    def vyx(self):
        """float : Poisson's ratio vxy in y-z directions [unitless]."""
        return self._vyx

    @property
    def vzx(self):
        """float : Poisson's ratio vxy in x-z directions [unitless]."""
        return self._vzx

    @property
    def Gxy(self):
        """float : Shear modulus Gxy in x-y directions, for example [Pa]."""
        return self._Gxy

    @property
    def Gyz(self):
        """float : Shear modulus Gxy in xy-z directions, for example [Pa]."""
        return self._Gyz

    @property
    def Gzx(self):
        """float : Shear modulus Gxy in x-z directions, for example [Pa]."""
        return self._Gzx

    @property
    def p(self):
        """float : Density, for example [kg/m3]."""
        return self._p


class ElasticIsotropicBase(MaterialBase):
    """Elastic, isotropic and homogeneous material.

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
    """

    def __init__(self, name, E, v, p):
        super(ElasticIsotropicBase, self).__init__(name=name)
        self.__name__ = 'ElasticIsotropic'
        self._E = E
        self._v = v
        self._G = 0.5 * E / (1 + v)
        self._p = p

    @property
    def E(self):
        """float : Young's modulus E, for example [Pa]."""
        return self._E

    @property
    def v(self):
        """float : Poisson's ratio v [unitless]."""
        return self._v

    @property
    def G(self):
        """float : Shear modulus  G, for example [Pa]."""
        return self._G

    @property
    def p(self):
        """float : Density, for example [kg/m3]."""
        return self._p


class StiffBase(ElasticIsotropicBase):
    """Elastic, very stiff and massless material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E, for example [Pa].
    """

    def __init__(self, name, E=10**13,  p=10**(-1)):  # FIXME: depending on the unit used, this is not be correct.
        super(StiffBase, self).__init__(name=name, E=E, v=0.3, p=p)
        self.__name__ = 'Stiff'


# ==============================================================================
# non-linear general
# ==============================================================================

class ElasticPlasticBase(ElasticIsotropicBase):
    """Elastic and plastic, isotropic and homogeneous material.

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
        super(ElasticPlasticBase, self).__init__(name=name, E=E, v=v, p=p)

        fc = [-i for i in f]
        ec = [-i for i in e]

        self.__name__ = 'ElasticPlastic'
        self._tension = {'f': f, 'e': e}
        self._compression = {'f': fc, 'e': ec}

    @property
    def tension(self):
        """dict : Parameters for modelling the tension side of the stess--strain curve"""
        return self._tension

    @property
    def compression(self):
        """dict : Parameters for modelling the tension side of the stess--strain curve"""
        return self._compression


# ==============================================================================
# non-linear metal
# ==============================================================================
# FIXME these are unit based! change
class SteelBase(ElasticIsotropicBase):
    """Bi-linear steel with given yield stress.

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

    Attributes
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    G : float
        Shear modulus G [Pa].
    fy : float
        Yield stress [MPa].
    fu : float
        Ultimate stress [MPa].
    eu : float
        Ultimate strain [%].
    ep : float
        Plastic strain [%].
    tension : dict
        Parameters for modelling the tension side of the stess--strain curve
    compression : dict
        Parameters for modelling the tension side of the stess--strain curve
    """

    def __init__(self, name, fy=355, fu=None, eu=20, E=210, v=0.3, p=7850):
        raise NotImplementedError
        super(SteelBase, self).__init__(name=name, E=E, v=v, p=p)

        E *= 10.**9
        fy *= 10.**6
        eu *= 0.01

        if not fu:
            fu = fy
        else:
            fu *= 10.**6

        ep = eu - fy / E
        f = [fy, fu]
        e = [0, ep]
        fc = [-i for i in f]
        ec = [-i for i in e]

        self.__name__ = 'Steel'
        self.name = name
        self.fy = fy
        self.fu = fu
        self.eu = eu
        self.ep = ep
        self.E = {'E': E}
        self.v = {'v': v}
        self.G = {'G': 0.5 * E / (1 + v)}
        self.p = p
        self.tension = {'f': f, 'e': e}
        self.compression = {'f': fc, 'e': ec}
        self.attr_list.extend(['fy', 'fu', 'eu', 'ep', 'E', 'v', 'G', 'p', 'tension', 'compression'])


# ==============================================================================
# non-linear timber
# ==============================================================================


# ==============================================================================
# non-linear masonry
# ==============================================================================


# ==============================================================================
# non-linear concrete
# ==============================================================================

class ConcreteBase(MaterialBase):
    """Elastic and plastic-cracking Eurocode based concrete material.

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

    Attributes
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    G : float
        Shear modulus G [Pa].
    fck : float
        Characteristic (5%) 28 day cylinder strength [MPa].
    fr : list
        Failure ratios.
    tension : dict
        Parameters for modelling the tension side of the stess--strain curve
    compression : dict
        Parameters for modelling the tension side of the stess--strain curve

    Notes
    -----
    - The concrete model is based on Eurocode 2 up to fck=90 MPa.
    """

    def __init__(self, name, fck, v=0.2, p=2400, fr=None):
        raise NotImplementedError
        MaterialBase.__init__(self, name=name)

        de = 0.0001
        fcm = fck + 8
        Ecm = 22 * 10**3 * (fcm / 10.)**0.3
        ec1 = min(0.7 * fcm**0.31, 2.8) * 0.001
        ecu1 = 0.0035 if fck < 50 else (2.8 + 27 * ((98 - fcm) / 100.)**4) * 0.001

        k = 1.05 * Ecm * ec1 / fcm
        e = [i * de for i in range(int(ecu1 / de) + 1)]
        ec = [ei - e[1] for ei in e[1:]]
        fctm = 0.3 * fck**(2. / 3.) if fck <= 50 else 2.12 * log(1 + fcm / 10.)
        f = [10**6 * fcm * (k * (ei / ec1) - (ei / ec1)**2) / (1. + (k - 2) * (ei / ec1)) for ei in e]

        E = f[1] / e[1]
        ft = [1., 0.]
        et = [0., 0.001]

        if not fr:
            fr = [1.16, fctm / fcm]

        self.__name__ = 'Concrete'
        self.name = name
        self.fck = fck * 10.**6
        self.E = {'E': E}
        self.v = {'v': v}
        self.G = {'G': 0.5 * E / (1 + v)}
        self.p = p
        self.tension = {'f': ft, 'e': et}
        self.compression = {'f': f[1:], 'e': ec}
        self.fratios = fr
        self.attr_list.extend(['fck', 'fratios', 'E', 'v', 'G', 'p', 'tension', 'compression'])


class ConcreteSmearedCrackBase(MaterialBase):
    """Elastic and plastic, cracking concrete material.

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

    Attributes
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    G : float
        Shear modulus G [Pa].
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
    tension : dict
        Parameters for modelling the tension side of the stess--strain curve
    compression : dict
        Parameters for modelling the tension side of the stess--strain curve
    """

    def __init__(self, name, E, v, p, fc, ec, ft, et, fr=[1.16, 0.0836]):
        raise NotImplementedError
        MaterialBase.__init__(self, name=name)

        self.__name__ = 'ConcreteSmearedCrack'
        self.name = name
        self.E = {'E': E}
        self.v = {'v': v}
        self.G = {'G': 0.5 * E / (1 + v)}
        self.p = p
        self.tension = {'f': ft, 'e': et}
        self.compression = {'f': fc, 'e': ec}
        self.fratios = fr
        self.attr_list.extend(['E', 'v', 'G', 'p', 'tension', 'compression', 'fratios'])


class ConcreteDamagedPlasticityBase(MaterialBase):
    """Damaged plasticity isotropic and homogeneous material.

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

    Attributes
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    G : float
        Shear modulus G [Pa].
    damage : list
        Damage parameters.
    hardening : list
        Compression hardening parameters.
    stiffening : list
        Tension stiffening parameters.
    """

    def __init__(self, name, E, v, p, damage, hardening, stiffening):
        raise NotImplementedError
        MaterialBase.__init__(self, name=name)

        self.__name__ = 'ConcreteDamagedPlasticity'
        self.name = name
        self.E = {'E': E}
        self.v = {'v': v}
        self.G = {'G': 0.5 * E / (1 + v)}
        self.p = p
        self.damage = damage
        self.hardening = hardening
        self.stiffening = stiffening
        self.attr_list.extend(['E', 'v', 'G', 'p', 'damage', 'hardening', 'stiffening'])


# ==============================================================================
# thermal
# ==============================================================================

class ThermalMaterialBase(MaterialBase):
    """Class for thermal material properties. [WIP]

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

    def __init__(self, name, conductivity, p, sheat):
        raise NotImplementedError
        MaterialBase.__init__(self, name=name)

        self.__name__ = 'ThermalMaterial'
        self.name = name
        self.conductivity = conductivity
        self.p = p
        self.sheat = sheat
        self.attr_list.extend(['p', 'conductivity', 'sheat'])
