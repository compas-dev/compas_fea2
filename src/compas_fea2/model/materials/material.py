from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod

from compas_fea2.base import FEAData


class Material(FEAData):
    """Initialises base Material object.

    Parameters
    ----------
    denisty : float
        Density of the material.

    Attributes
    ----------
    density : float
        Density of the material.

    """

    def __init__(self, *, density, **kwargs):
        super(Material, self).__init__(**kwargs)
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

    def __init__(self, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density, **kwargs):
        super(ElasticOrthotropic, self).__init__(density=density, **kwargs)
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

    def __init__(self, *, E, v, density, **kwargs):
        super(ElasticIsotropic, self).__init__(density=density, **kwargs)
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
    """

    def __init__(self, **kwargs):
        super(Stiff, self).__init__(E=1e+16, v=0.3, density=1e-16, **kwargs)

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

    def __init__(self, *, E, v, density, strain_stress, **kwargs):
        super(ElasticPlastic, self).__init__(E=E, v=v, density=density, **kwargs)
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
