from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas_fea2.utilities._utils import extend_docstring

class _Material(FEAData):
    """
    Note
    ----
    Materials are registered to a :class:`compas_fea2.model.Model`. The same
    material can be assigned to multiple sections and in different elements and
    parts.


    Basic Material parameters and attributes
    ========================================

    Parameters
    ----------
    denisty : float
        Density of the material.
    expansion : float, optional
        Thermal expansion coefficient, by default None.
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Other Parameters
    ----------------
    **kwargs : dict
        Backend dependent keyword arguments.
        See the individual backends for more information.

    Attributes
    ----------
    name : str, optional
        Uniqe identifier.
    density : float
        Density of the material.
    expansion : float
        Thermal expansion coefficient.
    key : int
        The key index of the material. It is automatically assigned to material
        once it is added to the model.
    model : :class:`compas_fea2.model.Model`
        The Model where the material is assigned.

    """

    def __init__(self, *, density, expansion=None, name=None, **kwargs):
        super(_Material, self).__init__(name=name, **kwargs)
        self.density = density
        self.expansion = expansion
        self._key = None

    @property
    def key(self):
        return self._key

    @property
    def model(self):
        return self._registration

    def __str__(self):
        return """
{}
{}
name        : {}
density     : {}
expansion   : {}
""".format(self.__class__.__name__, len(self.__class__.__name__) * '-', self.name, self.density, self.expansion)

    def __html__(self):
        return """<html>
<head></head>
<body><p>Hello World!</p></body>
</html>"""

# ==============================================================================
# linear elastic
# ==============================================================================
@extend_docstring(_Material)
class ElasticOrthotropic(_Material):
    """
    ElasticOrthotropic material
    ===========================
    Elastic, orthotropic and homogeneous material

    Additional paramenters and attributes:

    Parameters
    ----------
    Ex : float
        Young's modulus Ex in x direction.
    Ey : float
        Young's modulus Ey in y direction.
    Ez : float
        Young's modulus Ez in z direction.
    vxy : float
        Poisson's ratio vxy in x-y directions.
    vyz : float
        Poisson's ratio vyz in y-z directions.
    vzx : float
        Poisson's ratio vzx in z-x directions.
    Gxy : float
        Shear modulus Gxy in x-y directions.
    Gyz : float
        Shear modulus Gyz in y-z directions.
    Gzx : float
        Shear modulus Gzx in z-x directions.

    Attributes
    ----------
    Ex : float
        Young's modulus Ex in x direction.
    Ey : float
        Young's modulus Ey in y direction.
    Ez : float
        Young's modulus Ez in z direction.
    vxy : float
        Poisson's ratio vxy in x-y directions.
    vyz : float
        Poisson's ratio vyz in y-z directions.
    vzx : float
        Poisson's ratio vzx in z-x directions.
    Gxy : float
        Shear modulus Gxy in x-y directions.
    Gyz : float
        Shear modulus Gyz in y-z directions.
    Gzx : float
        Shear modulus Gzx in z-x directions.
    """

    def __init__(self, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density, expansion=None, name=None, **kwargs):
        super(ElasticOrthotropic, self).__init__(density=density, expansion=expansion, name=name, **kwargs)
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
name        : {}
density     : {}
expansion   : {}

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
           self.name, self.density, self.expansion,
           self.Ex, self.Ey, self.Ez, self.vxy, self.vyz, self.vzx, self.Gxy, self.Gyz, self.Gzx)

@extend_docstring(_Material)
class ElasticIsotropic(_Material):
    """
    Elastic, isotropic and homogeneous material
    ===========================================

    Parameters
    ----------
    E : float
        Young's modulus E.
    v : float
        Poisson's ratio v.

    Attributes
    ----------
    E : float
        Young's modulus E.
    v : float
        Poisson's ratio v.
    G : float
        Shear modulus (automatically computed from E and v)
    """

    def __init__(self, *, E, v, density, expansion=None, name=None, **kwargs):
        super(ElasticIsotropic, self).__init__(density=density, expansion=expansion, name=name, **kwargs)
        self.E = E
        self.v = v

    def __str__(self):
        return """
ElasticIsotropic Material
-------------------------
name        : {}
density     : {}
expansion   : {}

E : {}
v : {}
G : {}
""".format(self.name, self.density, self.expansion, self.E, self.v, self.G)

    @property
    def G(self):
        return 0.5 * self.E / (1 + self.v)

class Stiff(_Material):
    """Elastic, very stiff and massless material.
    """
    def __init__(self, *, density, expansion=None, name=None, **kwargs):
        raise NotImplementedError()


# ==============================================================================
# non-linear general
# ==============================================================================
@extend_docstring(_Material)
class ElasticPlastic(ElasticIsotropic):
    """
    ElasticPlastic
    ==============

    Elastic and plastic, isotropic and homogeneous material.

    Additional parameters and attributes.

    Parameters
    ----------
    E : float
        Young's modulus.
    v : float
        Poisson's ratio.
    strain_stress : list[tuple[float, float]]
        Strain-stress data, including elastic and plastic behaviour,
        in the form of strain/stress value pairs.

    Attributes
    ----------
    E : float
        Young's modulus.
    v : float
        Poisson's ratio.
    G : float
        Shear modulus (automatically computed from E and v)
    strain_stress : list[tuple[float, float]]
        Strain-stress data, including elastic and plastic behaviour,
        in the form of strain/stress value pairs.
    """

    def __init__(self, *, E, v, density, strain_stress, expansion=None, name=None, **kwargs):
        super(ElasticPlastic, self).__init__(E=E, v=v, density=density, expansion=expansion, name=name, **kwargs)
        self.strain_stress = strain_stress

    def __str__(self):
        return """
ElasticPlastic Material
-----------------------
name        : {}
density     : {}
expansion   : {}

E  : {}
v  : {}
G  : {}

strain_stress : {}
""".format(self.name, self.density, self.expansion, self.E, self.v, self.G, self.strain_stress)


# ==============================================================================
# User-defined Materials
# ==============================================================================
class UserMaterial(FEAData):
    """ User Defined Material. Tho implement this type of material, a
    separate subroutine is required

    """

    def __init__(self, name=None, **kwargs):
        super(UserMaterial, self).__init__(self, name=name, **kwargs)
        raise NotImplementedError('This class is not available for the selected backend plugin')
