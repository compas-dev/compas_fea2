
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


# NOTE: these classes are sometimes overwriting the _base ones because Abaqus offers internal ways of computing beam sections' properties

def _generate_beams_jobdata(obj, set_name, orientation, stype):
    """Generates the common string information for the input file of all the
    abaqus predefined beam sections.

    Parameters
    ----------
    obj : :class:`compas_fea2.model.sections.BeamSection`
        Section to write in the input file.
    set_name : str
        Name of the element set to which the section is assigned.
    orientation : str
        Section orientation information.
    stype : str
        Abaqus identifier for the section. This is used to automatically generate
        the sectional properties.

    Returns
    -------
    input file data line (str).
    """
    orientation_line = ', '.join([str(v) for v in orientation])
    return """** Section: {}
*Beam Section, elset={}, material={}, section={}
{}
{}""".format(obj.name, set_name, obj.material.name, stype, ', '.join([str(v) for v in obj._properties]), orientation_line)


# ==============================================================================
# 0D
# ==============================================================================
class AbaqusMassSection(MassSection):
    """Abaqus implementation of the :class:`MassSection`.\n"""
    __doc__ += MassSection.__doc__

    def __init__(self, mass, name=None, **kwargs):
        super(AbaqusMassSection, self).__init__(mass, name=name, **kwargs)

    def _generate_jobdata(self, set_name):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** Section: \"{}\"
*Mass, elset={}
{}\n""".format(self.name, set_name, self.mass)


class AbaqusSpringSection(SpringSection):
    """Abaqus implementation of the :class:`SpringSection`.\n"""
    __doc__ += SpringSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, forces=None, displacements=None, stiffness=None, name=None, **kwargs):
        super().__init__(forces, displacements, stiffness, name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Abaqus')

# ==============================================================================
# 1D
# ==============================================================================


class AbaqusBeamSection(BeamSection):
    """Abaqus implementation of the :class:`BeamSection`.\n"""
    __doc__ += BeamSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, name=None, **kwargs):
        super().__init__(A=A, Ixx=Ixx, Iyy=Iyy, Ixy=Ixy, Avx=Avx, Avy=Avy, J=J, g0=g0, gw=gw, material=material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Abaqus')


class AbaqusAngleSection(AngleSection):
    """Abaqus implementation of the :class:`AngleSection`.\n"""
    __doc__ += AngleSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, w, h, t, material, name=None, **kwargs):
        super(AbaqusAngleSection, self).__init__(w, h, t, material, name=name, **kwargs)
        if not isinstance(t, list):
            t = [t]*2
        self._properties = [w, h, *t]

    def _generate_jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, 'L')


class AbaqusBoxSection(BoxSection):
    """Abaqus implementation of the :class:`BoxSection`.\n"""
    __doc__ += BoxSection.__doc__
    __doc__ += """Box section.

    Note
    ----
    This is temporarily inconsistent with the base class. WIP

    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, w, h, t, material, **kwargs):
        super(AbaqusBoxSection, self).__init__(self, w, h, t, material, **kwargs)
        if not isinstance(t, list):
            t = [t]*4
        self._properties = [w, h, *self._t]

    def _generate_jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, 'box')


class AbaqusCircularSection(CircularSection):
    """Abaqus implementation of the :class:`CircularSection`.\n"""
    __doc__ += CircularSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, r, material, name=None, **kwargs):
        super(AbaqusCircularSection, self).__init__(r, material, name=name, **kwargs)
        self._properties = [r]

    def _generate_jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, 'circ')


class AbaqusHexSection(HexSection):
    """Abaqus implementation of the :class:`HexSection`.\n"""
    __doc__ += HexSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, r, t, material, name=None, **kwargs):
        super(AbaqusHexSection, self).__init__(r, t, material, name=name, **kwargs)
        self._stype = 'hex'
        self.properties = [r, t]


class AbaqusISection(ISection):
    """Abaqus implementation of the :class:`ISection`.\n"""
    __doc__ += ISection.__doc__
    __doc__ += """I or T section.

    Note
    ----
    This is temporarily inconsistent with the base class. WIP

    Note
    ----
    Set b1 and t1 or b2 and t2 to zero to model a T-section

    Note
    ----
    The section properties are automatically computed by Abaqus.
    """

    def __init__(self,  w, h, t, material, l=0, name=None, **kwargs):
        super(AbaqusISection, self).__init__(w, h, t, t, material, name=name, **kwargs)
        self._stype = 'I'
        if not isinstance(w, list):
            w = [w]*2
        if not isinstance(h, list):
            t = [t]*3
        self.properties = [l, h, *w, *t]


class AbaqusPipeSection(PipeSection):
    """Abaqus implementation of the :class:`PipeSection`.\n"""
    __doc__ += PipeSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, r, t, material, name=None, **kwarg):
        super(AbaqusPipeSection, self).__init__(r, t, material, name=name, **kwarg)
        self._stype = 'pipe'
        self.properties = [r, t]


class AbaqusRectangularSection(RectangularSection):
    """Abaqus implementation of the :class:`RectangularSection`.\n"""
    __doc__ += RectangularSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self,  w, h, material, name=None, **kwargs):
        super(AbaqusRectangularSection, self).__init__(w=w, h=h, material=material, name=name, **kwargs)
        self._properties = [w, h]

    def _generate_jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, 'rect')


class AbaqusTrapezoidalSection(TrapezoidalSection):
    """Abaqus implementation of the :class:`TrapezoidalSection`.\n"""
    __doc__ += TrapezoidalSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, w1, w2, h, material, name=None, **kwargs):
        super(AbaqusTrapezoidalSection, self).__init__(w1, w2, h, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Abaqus')


# TODO -> check how these sections are implemented in ABAQUS
class AbaqusTrussSection(TrussSection):
    """Abaqus implementation of the :class:`TrussSection`.\n"""
    __doc__ += TrussSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusTrussSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Abaqus')


class AbaqusStrutSection(StrutSection):
    """Abaqus implementation of the :class:`StrutSection`.\n"""
    __doc__ += StrutSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusStrutSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Abaqus')


class AbaqusTieSection(TieSection):
    """Abaqus implementation of the :class:`TieSection`.\n"""
    __doc__ += TieSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusTieSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError('{self.__class__.__name__} is not available in Abaqus')


# ==============================================================================
# 2D
# ==============================================================================

class AbaqusShellSection(ShellSection):
    """Abaqus implementation of the :class:`ShellSection`.\n"""
    __doc__ += ShellSection.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    int_points : int
        number of integration points. 5 by default.
    """

    def __init__(self, t, material, int_points=5, name=None, **kwargs):
        super(AbaqusShellSection, self).__init__(t, material, name=name, **kwargs)
        self.int_points = int_points

    def _generate_jobdata(self, set_name):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** Section: {}
*Shell Section, elset={}, material={}
{}, {}""".format(self.name, set_name, self.material.name, self.t, self.int_points)


class AbaqusMembraneSection(MembraneSection):
    """Abaqus implementation of the :class:`MembraneSection`.\n"""
    __doc__ += MembraneSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(AbaqusMembraneSection, self).__init__(t, material, name=name, **kwargs)

    def _generate_jobdata(self, set_name):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** Section: {}
*Membrane Section, elset={}, material={}
{},""".format(self.name, set_name, self.material.name, self.t)


# ==============================================================================
# 3D
# ==============================================================================

class AbaqusSolidSection(SolidSection):
    """Abaqus implementation of the :class:`SolidSection`.\n"""
    __doc__ += SolidSection.__doc__

    def __init__(self, material, name=None, **kwargs):
        super(AbaqusSolidSection, self).__init__(material, name=name, **kwargs)

    def _generate_jobdata(self, set_name):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** Section: {}
*Solid Section, elset={}, material={}
,""".format(self.name, set_name, self.material.name)
