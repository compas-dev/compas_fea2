from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import log
from .material import _Material


class Concrete(_Material):
    """Elastic and plastic-cracking Eurocode based concrete material.

    Parameters
    ----------
    name : str
        Material name.
    fck : float
        Characteristic (5%) 28 day cylinder strength [MPa].
    v : float
        Poisson's ratio v [-].
    density : float
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
    density : float
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

    def __init__(self, *, fck, v=0.2, density=2400, fr=None,  name=None, **kwargs):
        super(Concrete, self).__init__(density=density,  name=name, **kwargs)

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
""".format(self.name, self.density, self.E, self.v, self.G, self.fck, self.fr)


class ConcreteSmearedCrack(_Material):
    """Elastic and plastic, cracking concrete material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    density : float
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
    density : float
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

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], name=None, **kwargs):
        super(ConcreteSmearedCrack, self).__init__(density=density, name=name, **kwargs)

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
""".format(self.name, self.density, self.E, self.v, self.G, self.fc, self.ec, self.ft, self.et, self.fr)


class ConcreteDamagedPlasticity(_Material):
    """Damaged plasticity isotropic and homogeneous material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    density : float
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
    density : float
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

    def __init__(self, *, E, v, density, damage, hardening, stiffening, name=None, **kwargs):
        super(ConcreteDamagedPlasticity, self).__init__(density=density, name=name, **kwargs)

        self.E = E
        self.v = v

        # would make sense to validate these inputs
        self.damage = damage
        self.hardening = hardening
        self.stiffening = stiffening

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)
