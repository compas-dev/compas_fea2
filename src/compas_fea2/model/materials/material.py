from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod

from compas_fea2.base import FEABase


class Material(FEABase):
    """Initialises base Material object.

    Parameters
    ----------
    name : str
        Name of the Material object.

    """

    def __init__(self, name, *, density):
        super(Material, self).__init__(name=name)
        self.density = density

    def __str__(self):
        return """
{}
{}
name    : {}
density : {}
""".format(self.__class__.__name__, len(self.__class__.__name__) * '-', self.name, self.density)

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
    density : float
        Density [kg/m3].

    Warnings
    --------
    Can be created but is currently not implemented.

    """

    def __init__(self, name, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density):
        super(ElasticOrthotropic, self).__init__(name, density=density)
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
           self.name, self.density,
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
    density : float
        Density [kg/m3].

    Other Parameters
    ----------------
    **kwargs : dict
        Backend dependent keyword arguments.
        See the individual backends for more information.

    """

    def __init__(self, name, *, E, v, density, **kwargs):
        super(ElasticIsotropic, self).__init__(name, density=density)
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
""".format(self.name, self.density, self.E, self.v, self.G)

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
        super(Stiff, self).__init__(name, E=1e+16, v=0.3, density=1e-16)

    def __str__(self):
        return """
Stiff Material
--------------
name    : {}
density : {}

E : {}
v : {}
G : {}
""".format(self.name, self.density, self.E, self.v, self.G)


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
        Young's modulus [Pa].
    v : float
        Poisson's ratio [-].
    density : float
        Density [kg/m3].
    strain_stress : list[tuple[float, float]]
        Strain-stress data, including elastic and plastic behaviour,
        in the form of strain/stress value pairs.

    """

    def __init__(self, name, *, E, v, density, strain_stress):
        super(ElasticPlastic, self).__init__(name, E=E, v=v, density=density)
        self.strain_stress = strain_stress

    def __str__(self):
        return """
ElasticPlastic Material
-----------------------
name    : {}
density : {}

E  : {}
v  : {}
G  : {}

strain_stress : {}
""".format(self.name, self.density, self.E, self.v, self.G, self.strain_stress)
