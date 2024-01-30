from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2 import units
from .material import ElasticIsotropic


class Steel(ElasticIsotropic):
    """Bi-linear steel with given yield stress.

    Parameters
    ----------
    E : float
        Young's modulus E.
    v : float
        Poisson's ratio v.
    fy : float
        Yield stress.
    fu : float
        Ultimate stress.
    eu : float
        Ultimate strain.

    Additional Attributes
    ---------------------
    E : float
        Young's modulus E.
    v : float
        Poisson's ratio v.
    G : float
        Shear modulus G.
    fy : float
        Yield stress.
    fu : float
        Ultimate stress.
    eu : float
        Ultimate strain.
    ep : float
        Plastic strain.

    """

    def __init__(self, *, fy, fu, eu, E, v, density, **kwargs):
        super(Steel, self).__init__(E=E, v=v, density=density, **kwargs)

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
        self.tension = {"f": f, "e": e}
        self.compression = {"f": fc, "e": ec}

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
""".format(
            self.name,
            (self.density * units["kg/m**2"]),
            (self.E * units.pascal).to("GPa"),
            (self.G * units.pascal).to("GPa"),
            (self.fy * units.pascal).to("MPa"),
            (self.fu * units.pascal).to("MPa"),
            (self.v * units.dimensionless),
            (self.eu * units.dimensionless),
            (self.ep * units.dimensionless),
        )

    # TODO check values and make unit independent
    @classmethod
    def S355(cls):
        """Steel S355.

        Returns
        -------
        :class:`compas_fea2.model.material.Steel`
            The precompiled steel material.
        """
        return cls(fy=355, fu=None, eu=20, E=210, v=0.3, density=7850, name=None)
