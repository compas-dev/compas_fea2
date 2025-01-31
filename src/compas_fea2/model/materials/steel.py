from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.units import UnitRegistry
from compas_fea2.units import units as u

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
    density : float, optional
        Density of the steel material [kg/m^3].
    name : str, optional
        Name of the material.

    Attributes
    ----------
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
    tension : dict
        Parameters for modelling the tension side of the stress-strain curve.
    compression : dict
        Parameters for modelling the compression side of the stress-strain curve.
    """

    def __init__(self, *, E, v, density, fy, fu, eu, **kwargs):
        super(Steel, self).__init__(E=E, v=v, density=density, **kwargs)

        fu = fu or fy

        # E *= 10**9
        # fu *= 10**6
        # fy *= 10**6
        # eu *= 0.01

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
density : {:.2f}

E  : {:.2f}
G  : {:.2f}
fy : {:.2f}
fu : {:.2f}
v  : {:.2f}
eu : {:.2f}
ep : {:.2f}
""".format(
            self.name,
            self.density,
            self.E,
            self.G,
            self.fy,
            self.fu,
            self.v,
            self.eu,
            self.ep,
        )

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "fy": self.fy,
                "fu": self.fu,
                "eu": self.eu,
                "ep": self.ep,
                "tension": self.tension,
                "compression": self.compression,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        return cls(
            E=data["E"],
            v=data["v"],
            density=data["density"],
            fy=data["fy"],
            fu=data["fu"],
            eu=data["eu"],
        )

    # TODO check values and make unit independent
    @classmethod
    def S355(cls, units=None):
        """Steel S355.

        Returns
        -------
        :class:`compas_fea2.model.material.Steel`
            The precompiled steel material.
        """
        if not units:
            units = u(system="SI_mm")
        elif not isinstance(units, UnitRegistry):
            units = u(system=units)

        return cls(fy=355 * units.MPa, fu=None, eu=20, E=210 * units.GPa, v=0.3, density=7850 * units("kg/m**3"), name=None)
