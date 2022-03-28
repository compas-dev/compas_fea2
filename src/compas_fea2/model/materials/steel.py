from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2 import units
from .material import ElasticIsotropic


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
    density : float
        Density [kg/m3].

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
    fy : float
        Yield stress [MPa].
    fu : float
        Ultimate stress [MPa].
    eu : float
        Ultimate strain [%].
    ep : float
        Plastic strain [%].

    """

    def __init__(self, *, fy, fu, eu, E, v, density, name=None, **kwargs):
        super(Steel, self).__init__(E=E, v=v, density=density, name=None, **kwargs)

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
           (self.density * units['kg/m**2']),
           (self.E * units.pascal).to('GPa'),
           (self.G * units.pascal).to('GPa'),
           (self.fy * units.pascal).to('MPa'),
           (self.fu * units.pascal).to('MPa'),
           (self.v * units.dimensionless),
           (self.eu * units.dimensionless),
           (self.ep * units.dimensionless))

    @staticmethod
    def S355(name='S355'):
        return Steel(name=name, fy=355, fu=None, eu=20, E=210, v=0.3, density=7850)
