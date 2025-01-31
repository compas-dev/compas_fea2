from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import log

from compas_fea2.units import UnitRegistry
from compas_fea2.units import units as u

from .material import _Material


class Concrete(_Material):
    """Elastic and plastic-cracking Eurocode-based concrete material.

    Parameters
    ----------
    fck : float
        Characteristic (5%) 28-day cylinder strength [MPa].
    v : float, optional
        Poisson's ratio v [-].
    fr : list, optional
        Failure ratios.
    density : float, optional
        Density of the concrete material [kg/m^3].
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
    fck : float
        Characteristic (5%) 28-day cylinder strength.
    fr : list
        Failure ratios.
    tension : dict
        Parameters for modeling the tension side of the stress-strain curve.
    compression : dict
        Parameters for modeling the compression side of the stress-strain curve.

    Notes
    -----
    The concrete model is based on Eurocode 2 up to fck=90 MPa.
    """

    def __init__(self, *, fck, E=None, v=None, density=None, fr=None, units=None, **kwargs):
        super(Concrete, self).__init__(density=density, **kwargs)

        # Ensure small increment for stress-strain curve
        de = 0.0001

        # Compute material properties based on Eurocode 2
        fcm = fck + 8  # Mean compressive strength
        Ecm = 22 * 10**3 * (fcm / 10) ** 0.3  # Young's modulus [MPa]
        ec1 = min(0.7 * fcm**0.31, 2.8) * 0.001  # Strain at peak stress
        ecu1 = 0.0035 if fck < 50 else (2.8 + 27 * ((98 - fcm) / 100.0) ** 4) * 0.001  # Ultimate strain

        # Stress-strain model parameters
        k = 1.05 * Ecm * ec1 / fcm
        e = [i * de for i in range(int(ecu1 / de) + 1)]  # Strain values
        ec = [ei - e[1] for ei in e[1:]] if len(e) > 1 else [0.0]  # Adjusted strain values

        # Tensile strength according to Eurocode 2
        fctm = 0.3 * fck ** (2 / 3) if fck <= 50 else 2.12 * log(1 + fcm / 10)  # Tensile strength
        fc = [10**6 * fcm * (k * (ei / ec1) - (ei / ec1) ** 2) / (1 + (k - 2) * (ei / ec1)) for ei in ec]

        ft = [1.0, 0.0]  # Tension stress-strain curve
        et = [0.0, 0.001]  # Corresponding strain values for tension

        fr = fr or [1.16, fctm / fcm]  # Failure ratios default

        # Assign attributes
        # BUG: change the units
        self.E = Ecm * 10**6 if E is None else E  # Convert GPa to MPa
        self.fck = fck * 10**6  # Convert MPa to Pascals
        self.fc = kwargs.get("fc", fc)
        self.ec = kwargs.get("ec", ec)
        self.v = v if v is not None else 0.17
        self.ft = kwargs.get("ft", ft)
        self.et = kwargs.get("et", et)
        self.fr = kwargs.get("fr", fr)

        # Ensure valid Young’s modulus calculation
        if len(self.fc) > 1 and self.fc[1] == 0:
            raise ValueError("fc[1] must be non-zero to calculate E.")
        if len(self.ec) > 1 and self.ec[1] == 0:
            raise ValueError("ec[1] must be non-zero for correct calculations.")

        # Tension and compression dictionaries
        self.tension = {"f": self.ft, "e": self.et}
        self.compression = {"f": self.fc[1:], "e": self.ec}

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
""".format(
            self.name, self.density, self.E, self.v, self.G, self.fck, self.fr
        )

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "fck": self.fck,
                "E": self.E,
                "v": self.v,
                "fr": self.fr,
                "tension": self.tension,
                "compression": self.compression,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        return cls(
            fck=data["fck"],
            E=data["E"],
            v=data["v"],
            density=data["density"],
            fr=data["fr"],
        )

    # FIXME: this is only working for the basic material properties.
    @classmethod
    def C20_25(cls, units, **kwargs):
        if not units:
            units = u.get_default_units()
        elif not isinstance(units, UnitRegistry):
            units = u.get_units(units)

        return cls(fck=25 * units.MPa, E=30 * units.GPa, v=0.17, density=2400 * units("kg/m**3"), name="C20/25", **kwargs)


class ConcreteSmearedCrack(_Material):
    """Elastic and plastic, cracking concrete material.

    Parameters
    ----------
    E : float
        Young's modulus E.
    v : float
        Poisson's ratio v.
    fc : list
        Plastic stress data in compression.
    ec : list
        Plastic strain data in compression.
    ft : list
        Plastic stress data in tension.
    et : list
        Plastic strain data in tension.
    fr : list, optional
        Failure ratios.
    density : float, optional
        Density of the concrete material [kg/m^3].
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
    fc : list
        Plastic stress data in compression.
    ec : list
        Plastic strain data in compression.
    ft : list
        Plastic stress data in tension.
    et : list
        Plastic strain data in tension.
    fr : list
        Failure ratios.
    tension : dict
        Parameters for modelling the tension side of the stress-strain curve.
    compression : dict
        Parameters for modelling the compression side of the stress-strain curve.
    """

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], **kwargs):
        super(ConcreteSmearedCrack, self).__init__(density=density, **kwargs)

        self.E = E
        self.v = v
        self.fc = fc
        self.ec = ec
        self.ft = ft
        self.et = et
        self.fr = fr
        # are these necessary if we have the above?
        self.tension = {"f": ft, "e": et}
        self.compression = {"f": fc, "e": ec}

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
""".format(
            self.name, self.density, self.E, self.v, self.G, self.fc, self.ec, self.ft, self.et, self.fr
        )

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "class": self.__class__.__name__,
                "E": self.E,
                "v": self.v,
                "fc": self.fc,
                "ec": self.ec,
                "ft": self.ft,
                "et": self.et,
                "fr": self.fr,
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
            fc=data["fc"],
            ec=data["ec"],
            ft=data["ft"],
            et=data["et"],
            fr=data["fr"],
            name=data["name"],
        )


class ConcreteDamagedPlasticity(_Material):
    """Damaged plasticity isotropic and homogeneous material.

    Parameters
    ----------
    E : float
        Young's modulus E.
    v : float
        Poisson's ratio v.
    damage : list
        Damage parameters.
    hardening : list
        Compression hardening parameters.
    stiffening : list
        Tension stiffening parameters.
    density : float, optional
        Density of the concrete material [kg/m^3].
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
    damage : list
        Damage parameters.
    hardening : list
        Compression hardening parameters.
    stiffening : list
        Tension stiffening parameters.
    """

    def __init__(self, *, E, v, density, damage, hardening, stiffening, **kwargs):
        super(ConcreteDamagedPlasticity, self).__init__(density=density, **kwargs)

        self.E = E
        self.v = v

        # TODO would make sense to validate these inputs
        self.damage = damage
        self.hardening = hardening
        self.stiffening = stiffening

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "class": self.__class__.__name__,
                "E": self.E,
                "v": self.v,
                "damage": self.damage,
                "hardening": self.hardening,
                "stiffening": self.stiffening,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        return cls(
            E=data["E"],
            v=data["v"],
            density=data["density"],
            damage=data["damage"],
            hardening=data["hardening"],
            stiffening=data["stiffening"],
            name=data["name"],
        )
