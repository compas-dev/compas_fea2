from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import log
from abc import abstractmethod

from compas_fea2 import units
from compas_fea2.base import FEABase


class Material(FEABase):
    """Initialises base Material object.

    Parameters
    ----------
    name : str
        Name of the Material object.

    """

    def __init__(self, name, *, p):
        super(Material, self).__init__(name=name)
        self.p = p

    def __str__(self):
        return """
{}
{}
name    : {}
density : {}
""".format(self.__class__.__name__, len(self.__class__.__name__) * '-', self.name, self.p)

    @abstractmethod
    def jobdata(self, *args, **kwargs):
        """Generate the job data for the backend-specific input file."""
        raise NotImplementedError


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticOrthotropic(Material):
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

    def __init__(self, name, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, p):
        super(ElasticOrthotropic, self).__init__(name, p=p)
        self.Ex = Ex
        self.Ey = Ey
        self.Ez = Ez
        self.vxy = vxy
        self.vyz = vyz
        self.vzx = vzx
        self.Gxy = Gxy
        self.Gyz = Gyz
        self.Gzx = Gzx

    def __str__(self):
        return """
{}
{}
name    : {}
density : {}

Ex  : {}
Ey  : {}
Ez  : {}
vxy : {}
vyz : {}
vzx : {}
Gxy : {}
Gyz : {}
Gzx : {}
""".format(self.__class__.__name__, len(self.__class__.__name__) * '-',
           self.name, self.p,
           self.Ex, self.Ey, self.Ez, self.vxy, self.vyz, self.vzx, self.Gxy, self.Gyz, self.Gzx)


class ElasticIsotropic(Material):
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

    Other Parameters
    ----------------
    **kwargs : dict
        Backend dependent keyword arguments.
        See the individual backends for more information.

    """

    def __init__(self, name, *, E, v, p, **kwargs):
        super(ElasticIsotropic, self).__init__(name, p=p)
        self.E = E
        self.v = v

    def __str__(self):
        return """
ElasticIsotropic Material
-------------------------
name    : {}
density : {}

E : {}
v : {}
G : {}
""".format(self.name, self.p, self.E, self.v, self.G)

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)


class Stiff(ElasticIsotropic):
    """Elastic, very stiff and massless material.

    Parameters
    ----------
    name : str
        Material name.

    """

    def __init__(self, name):
        super(Stiff, self).__init__(name, E=1e+16, v=0.3, p=1e-16)

    def __str__(self):
        return """
Stiff Material
--------------
name    : {}
density : {}

E : {}
v : {}
G : {}
""".format(self.name, self.p, self.E, self.v, self.G)


# ==============================================================================
# non-linear general
# ==============================================================================

class ElasticPlastic(ElasticIsotropic):
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

    def __init__(self, name, *, E, v, p, f, e):
        super(ElasticPlastic, self).__init__(name, E=E, v=v, p=p)
        self.fc = fc = [-i for i in f]
        self.ec = ec = [-i for i in e]
        self.tension = {'f': f, 'e': e}
        self.compression = {'f': fc, 'e': ec}

    def __str__(self):
        return """
ElasticPlastic Material
-----------------------
name    : {}
density : {}

E  : {}
v  : {}
G  : {}
fc : {}
ec : {}
""".format(self.name, self.p, self.E, self.v, self.G, self.fc, self.ec)


# ==============================================================================
# non-linear metal
# ==============================================================================

class Steel(ElasticIsotropic):
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

    def __init__(self, name, *, fy, fu, eu, E, v, p):
        super(Steel, self).__init__(name, E=E, v=v, p=p)

        fu = fu or fy

        E *= 10**9
        fu *= 10**6
        fy *= 10**6
        eu *= 0.01

        ep = eu - fy / E
        f = [fy, fu]
        e = [0, ep]
        fc = [-i for i in f]
        ec = [-i for i in e]

        self.fy = fy
        self.fu = fu
        self.eu = eu
        self.ep = ep
        self.E = E
        self.v = v
        self.tension = {'f': f, 'e': e}
        self.compression = {'f': fc, 'e': ec}

    def __str__(self):
        return """
Steel Material
--------------
name    : {}
density : {:~.0f}

E  : {:~.0f}
G  : {:~.0f}
fy : {:~.0f}
fu : {:~.0f}
v  : {:.2f}
eu : {:.2f}
ep : {:.2f}
""".format(self.name,
           (self.p * units['kg/m**2']),
           (self.E * units.pascal).to('GPa'),
           (self.G * units.pascal).to('GPa'),
           (self.fy * units.pascal).to('MPa'),
           (self.fu * units.pascal).to('MPa'),
           (self.v * units.dimensionless),
           (self.eu * units.dimensionless),
           (self.ep * units.dimensionless))

    @staticmethod
    def S355(name='S355'):
        return Steel(name=name, fy=355, fu=None, eu=20, E=210, v=0.3, p=7850)


# ==============================================================================
# non-linear timber
# ==============================================================================


# ==============================================================================
# non-linear masonry
# ==============================================================================


# ==============================================================================
# non-linear concrete
# ==============================================================================

class Concrete(Material):
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

    def __init__(self, name, *, fck, v=0.2, p=2400, fr=None):
        super(Concrete, self).__init__(name, p=p)

        de = 0.0001
        fcm = fck + 8
        Ecm = 22 * 10**3 * (fcm / 10)**0.3
        ec1 = min(0.7 * fcm**0.31, 2.8) * 0.001
        ecu1 = 0.0035 if fck < 50 else (2.8 + 27 * ((98 - fcm) / 100.)**4) * 0.001

        k = 1.05 * Ecm * ec1 / fcm
        e = [i * de for i in range(int(ecu1 / de) + 1)]
        ec = [ei - e[1] for ei in e[1:]]
        fctm = 0.3 * fck**(2 / 3) if fck <= 50 else 2.12 * log(1 + fcm / 10)
        f = [10**6 * fcm * (k * (ei / ec1) - (ei / ec1)**2) / (1 + (k - 2) * (ei / ec1)) for ei in e]

        E = f[1] / e[1]
        ft = [1.0, 0.0]
        et = [0.0, 0.001]
        fr = fr or [1.16, fctm / fcm]

        self.fck = fck * 10**6
        self.E = E
        self.v = v
        self.fc = f
        self.ec = ec
        self.ft = ft
        self.et = et
        self.fr = fr
        # these necessary if we have the above?
        self.tension = {'f': ft, 'e': et}
        self.compression = {'f': f[1:], 'e': ec}

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)

    def __str__(self):
        return """
Concrete Material
-----------------
name    : {}
density : {}

E   : {}
v   : {}
G   : {}
fck : {}
fr  : {}
""".format(self.name, self.p, self.E, self.v, self.G, self.fck, self.fr)


class ConcreteSmearedCrack(Material):
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

    def __init__(self, name, *, E, v, p, fc, ec, ft, et, fr=[1.16, 0.0836]):
        super(ConcreteSmearedCrack, self).__init__(name, p=p)

        self.E = E
        self.v = v
        self.fc = fc
        self.ec = ec
        self.ft = ft
        self.et = et
        self.fr = fr
        # are these necessary if we have the above?
        self.tension = {'f': ft, 'e': et}
        self.compression = {'f': fc, 'e': ec}

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)

    def __str__(self):
        return """
Concrete Material
-----------------
name    : {}
density : {}

E  : {}
v  : {}
G  : {}
fc : {}
ec : {}
ft : {}
et : {}
fr : {}
""".format(self.name, self.p, self.E, self.v, self.G, self.fc, self.ec, self.ft, self.et, self.fr)


class ConcreteDamagedPlasticity(Material):
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

    def __init__(self, name, *, E, v, p, damage, hardening, stiffening):
        super(ConcreteDamagedPlasticity, self).__init__(name, p=p)

        self.E = E
        self.v = v

        # would make sense to validate these inputs
        self.damage = damage
        self.hardening = hardening
        self.stiffening = stiffening

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)


# ==============================================================================
# thermal
# ==============================================================================

class ThermalMaterial(Material):
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

    def __init__(self, name, *, conductivity, p, sheat):
        super(ThermalMaterial, self).__init__(name, p=p)

        # all these list inputs should be validated
        self.conductivity = conductivity
        self.sheat = sheat
