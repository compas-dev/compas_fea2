
from compas_fea2.model import Section
from compas_fea2.model import BeamSection
from compas_fea2.model import AngleSection
from compas_fea2.model import BoxSection
# from compas_fea2.model import HexSection
from compas_fea2.model import ISection
from compas_fea2.model import CircularSection
from compas_fea2.model import MassSection
from compas_fea2.model import ShellSection
from compas_fea2.model import MembraneSection
from compas_fea2.model import SolidSection
from compas_fea2.model import TrussSection
from compas_fea2.model import StrutSection
from compas_fea2.model import TieSection
from compas_fea2.model import SpringSection


# NOTE: these classes are sometimes overwriting the _base ones because Abaqus
# offers internal ways of computing beam sections' properties

def _generate_beams_jobdata(obj, set_name, orientation, stype):
    """Generates the string information for the input file.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).
    """
    orientation_line = ', '.join([str(v) for v in orientation])
    return """** Section: {}
*Beam Section, elset={}, material={}, section={}
{}\n{}\n""".format(obj.name, set_name, obj.material.name, stype, ', '.join([str(v) for v in obj._properties]), orientation_line)


# ==============================================================================
# 0D
# ==============================================================================
class AbaqusMassSection(MassSection):
    """Section for mass elements.

    Parameters
    ----------
    name : str
        Section name.
    mass : float
        Point mass value.
    """

    def __init__(self, name, mass):
        super(AbaqusMassSection, self).__init__(name, mass)

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
*Mass, elset={}
{}\n""".format(self.name, set_name, self.mass)


# ==============================================================================
# 1D
# ==============================================================================

class AbaqusAngleSection(AngleSection):
    """
    """

    def __init__(self, name, w, h, t, material, **kwargs):
        super(AbaqusAngleSection, self).__init__(name, w, h, t, material, **kwargs)
        if not isinstance(t, list):
            t = [t]*2
        self._properties = [w, h, *t]

    def _generate_jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, 'L')


# class AbaqusBoxSection(BoxSection):
#     """Box section.

#     Parameters
#     ----------
#     b : float
#         base of the section.
#     h : float
#         total height of the section (including the flanges).
#     t : float or list
#         thickness(es) of the section. If the four thicknesses are different,
#         provide a list the four values [t1, t2, t3, t4]
#     material : str
#         material name to be assigned to the section.

#     """

#     def __init__(self, w, h, t, material, **kwargs):
#         super(AbaqusBoxSection, self).__init__(self, w, h, t, material, **kwargs)
#         if not isinstance(t, list):
#             t = [t]*4
#         self._properties = [w, h, *self._t]

#     def _generate_jobdata(self, set_name, orientation):
#         return _generate_beams_jobdata(self, set_name, orientation, 'box')


class AbaqusCircularSection(CircularSection):
    """Circular filled section.

    Parameters
    ----------
    r : float
        outside radius
    material : str
        material name to be assigned to the section.
    """

    def __init__(self, r, material):
        super(AbaqusCircularSection, self).__init__(r, material)
        self.properties = [r]

    def _generate_jobdata(self, set_name, orientation):
        return _generate_beams_jobdata(self, set_name, orientation, 'circ')


# class AbaqusHexSection(HexSection):
#     """Hexagonal hollow section.

#     Parameters
#     ----------
#     r : float
#         outside radius
#     t : float
#         wall thickness
#     material : str
#         material name to be assigned to the section.

#     """

#     def __init__(self, name, r, t, material):
#         super(AbaqusHexSection, self).__init__(name, r, material)
#         self._stype = 'hex'
#         self.properties = [r, t]


# class AbaqusISection(ISection):
#     """I or T section.

#     Parameters
#     ----------
#     b : float or list
#         base(s) of the section. If the two bases are different, provide a list
#         with the two values [b1, b2]
#     h : float
#         total height of the section (including the flanges).
#     t : float or list
#         thickness(es) of the section. If the three thicknesses are different,
#         provide a list the three values [t1, t2, t3]
#     material : str
#         material name to be assigned to the section.
#     l : float, optional
#         distance of the origin of the local cross-section axis from the origin
#         of the beam axis along the 2-axis, by default 0.

#     Notes
#     -----
#     Set b1 and t1 or b2 and t2 to zero to model a T-section
#     """

#     def __init__(self, name, b, h, t, material, l=0):
#         super(AbaqusISection, self).__init__(name, material)
#         self._stype = 'I'
#         if not isinstance(b, list):
#             b = [b]*2
#         if not isinstance(t, list):
#             t = [t]*3
#         self.properties = [l, h, *b, *t]


# class AbaqusPipeSection(AbaqusBeamSection):
#     """Pipe section.

#     Parameters
#     ----------
#     r : float
#         outside radius
#     t : float
#         wall thickness
#     material : str
#         material name to be assigned to the section.
#     """

#     def __init__(self, name, r, t, material):
#         super(AbaqusPipeSection, self).__init__(name, material)
#         self._stype = 'pipe'
#         self.properties = [r, t]


# class AbaqusRectangularSection(AbaqusBeamSection):
#     """Rectangular filled section.

#     Parameters
#     ----------
#     a : float
#         base of the section.
#     b : float
#         height of the section.
#     material : str
#         material name to be assigned to the section.
#     """

#     def __init__(self, name, b, h, material):
#         super(AbaqusRectangularSection, self).__init__(name, material)
#         self._stype = 'rect'
#         self.properties = [b, h]


# class AbaqusTrapezoidalSection(AbaqusBeamSection):
#     """Rectangular filled section.

#     Parameters
#     ----------
#     a : float
#         bottom base of the section.
#     b : float
#         height of the section.
#     c : float
#         top base of the section.
#     d : float
#         distance of the origin of the local cross-section axis from the origin
#         of the beam axis along the 2-axis, by default 0.
#     material : str
#         material name to be assigned to the section.
#     """

#     def __init__(self, name, a, b, c, d, material):
#         super(AbaqusTrapezoidalSection, self).__init__(name, material)
#         self._stype = 'rect'
#         self.properties = [a, b, c, d]


# TODO -> check how these sections are implemented in ABAQUS
class AbaqusTrussSection(TrussSection):

    def __init__(self, name, A, material):
        super(AbaqusTrussSection, self).__init__(name, A, material)
        raise NotImplementedError


class AbaqusStrutSection(StrutSection):

    def __init__(self, name, A, material):
        super(AbaqusStrutSection, self).__init__(name, A, material)
        raise NotImplementedError


class AbaqusTieSection(TieSection):

    def __init__(self, name, A, material):
        super(AbaqusTieSection, self).__init__(name, A, material)
        raise NotImplementedError


class AbaqusSpringSection(SpringSection):

    def __init__(self, name, forces={}, displacements={}, stiffness={}):
        super(AbaqusSpringSection, self).__init__(name, forces={}, displacements={}, stiffness={})
        raise NotImplementedError


# ==============================================================================
# 2D
# ==============================================================================

class AbaqusShellSection(ShellSection):
    """"""
    __doc__ += ShellSection.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    int_points : int
        number of integration points. 5 by default.
    """

    def __init__(self, name, t, material, int_points=5):
        super(AbaqusShellSection, self).__init__(name, t, material)
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
{}, {}\n""".format(self.name, set_name, self.material.name, self.t, self.int_points)


class AbaqusMembraneSection(MembraneSection):

    def __init__(self, name, t, material):
        super(AbaqusMembraneSection, self).__init__(name, t, material)

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
{},\n""".format(self.name, set_name, self.material.name, self.t)


# ==============================================================================
# 3D
# ==============================================================================

class AbaqusSolidSection(SolidSection):

    def __init__(self, name, material):
        super(AbaqusSolidSection, self).__init__(name, material)

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
,\n""".format(self.name, set_name, self.material.name)
