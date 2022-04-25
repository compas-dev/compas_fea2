
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import BeamSection
from compas_fea2.model import AngleSection
from compas_fea2.model import BoxSection
from compas_fea2.model import HexSection
from compas_fea2.model import ISection
from compas_fea2.model import CircularSection
from compas_fea2.model import RectangularSection
from compas_fea2.model import MassSection
from compas_fea2.model import ShellSection
from compas_fea2.model import MembraneSection
from compas_fea2.model import SolidSection
from compas_fea2.model import TrussSection
from compas_fea2.model import TrapezoidalSection
from compas_fea2.model import StrutSection
from compas_fea2.model import TieSection
from compas_fea2.model import SpringSection
from compas_fea2.model import PipeSection


# NOTE in opensees the sectional properties are assigned directly to the element UNLESS it is a nonliner thing...
# in that case there is a tag for the section....aaaaarrrrhhhh

# ==============================================================================
# 0D
# ==============================================================================
class OpenseesMassSection(MassSection):
    """"""
    __doc__ += MassSection.__doc__

    def __init__(self, mass, name=None, **kwargs):
        super(OpenseesMassSection, self).__init__(mass, name=name, **kwargs)


class OpenseesSpringSection(SpringSection):
    """"""
    __doc__ += SpringSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, forces=None, displacements=None, stiffness=None, name=None, **kwargs):
        super().__init__(forces, displacements, stiffness, name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Opensees')

# ==============================================================================
# 1D
# ==============================================================================


class OpenseesBeamSection(BeamSection):
    """"""
    __doc__ += BeamSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, name=None, **kwargs):
        super().__init__(A=A, Ixx=Ixx, Iyy=Iyy, Ixy=Ixy, Avx=Avx, Avy=Avy, J=J, g0=g0, gw=gw, material=material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Opensees')


class OpenseesAngleSection(AngleSection):
    """"""
    __doc__ += AngleSection.__doc__

    def __init__(self, w, h, t, material, name=None, **kwargs):
        super(OpenseesAngleSection, self).__init__(w, h, t, material, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesBoxSection(BoxSection):
    """"""
    __doc__ += BoxSection.__doc__

    def __init__(self, w, h, t, material, **kwargs):
        super(OpenseesBoxSection, self).__init__(self, w, h, t, material, **kwargs)
        raise NotImplementedError()


class OpenseesCircularSection(CircularSection):
    """"""
    __doc__ += CircularSection.__doc__

    def __init__(self, r, material, name=None, **kwargs):
        super(OpenseesCircularSection, self).__init__(r, material, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesHexSection(HexSection):
    """"""
    __doc__ += HexSection.__doc__

    def __init__(self, r, t, material, name=None, **kwargs):
        super(OpenseesHexSection, self).__init__(r, t, material, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesISection(ISection):
    """"""
    __doc__ += ISection.__doc__

    def __init__(self,  w, h, t, material, l=0, name=None, **kwargs):
        super(OpenseesISection, self).__init__(w, h, t, t, material, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesPipeSection(PipeSection):
    """"""
    __doc__ += PipeSection.__doc__

    def __init__(self, r, t, material, name=None, **kwarg):
        super(OpenseesPipeSection, self).__init__(r, t, material, name=name, **kwarg)
        raise NotImplementedError()


class OpenseesRectangularSection(RectangularSection):
    """OpenSees implementation of :class:`RectangularSection`. \n
    """
    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, name=None, **kwargs):
        super(OpenseesRectangularSection, self).__init__(w, h, material, name=None, **kwargs)

    def _generate_jobdata(self):
        return f'section Elastic {self.name} {self.material.E} {self.A} {self.Iyy} {self.Ixx} {self.material.G} {self.J}'


class OpenseesTrapezoidalSection(TrapezoidalSection):
    """"""
    __doc__ += TrapezoidalSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, w1, w2, h, material, name=None, **kwargs):
        super(OpenseesTrapezoidalSection, self).__init__(w1, w2, h, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Opensees')


# TODO -> check how these sections are implemented in ABAQUS
class OpenseesTrussSection(TrussSection):
    """"""
    __doc__ += TrussSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(OpenseesTrussSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Opensees')


class OpenseesStrutSection(StrutSection):
    """"""
    __doc__ += StrutSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(OpenseesStrutSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Opensees')


class OpenseesTieSection(TieSection):
    """"""
    __doc__ += TieSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Opensees.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(OpenseesTieSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Opensees')


# ==============================================================================
# 2D
# ==============================================================================

class OpenseesShellSection(ShellSection):
    """"""
    __doc__ += ShellSection.__doc__

    def __init__(self, t, material, int_points=5, name=None, **kwargs):
        super(OpenseesShellSection, self).__init__(t, material, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesMembraneSection(MembraneSection):
    """"""
    __doc__ += MembraneSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(OpenseesMembraneSection, self).__init__(t, material, name=name, **kwargs)
        raise NotImplementedError()

# ==============================================================================
# 3D
# ==============================================================================


class OpenseesSolidSection(SolidSection):
    """"""
    __doc__ += SolidSection.__doc__

    def __init__(self, material, name=None, **kwargs):
        super(OpenseesSolidSection, self).__init__(material, name=name, **kwargs)
        raise NotImplementedError()
