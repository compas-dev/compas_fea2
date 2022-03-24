from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import MassElement
from compas_fea2.model import BeamElement
from compas_fea2.model import SpringElement
from compas_fea2.model import TrussElement
from compas_fea2.model import ShellElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import SolidElement


# ==============================================================================
# 0D elements
# ==============================================================================

class AbaqusMassElement(MassElement):
    """A 0D element for concentrated point mass.

    Parameters
    ----------
    key : int
        Number of the element.
    elset : str
        Name of the automatically generated element set where the masses is applied.
    mass : float
        Concentrated mass (mass of each point of the set).

    """

    def __init__(self, key, node, mass, elset):
        super(AbaqusMassElement, self).__init__(key, node, mass, elset)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """
*ELEMENT, TYPE=MASS, ELSET={0}
{0}, {1}
*MASS, ELSET={0}
{1}
""".format(self.elset, self.node)


# ==============================================================================
# 1D elements
# ==============================================================================

class AbaqusBeamElement(BeamElement):

    def __init__(self, nodes, section, frame=[0.0, 0.0, -1.0], part=None, **kwargs):
        super(AbaqusBeamElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, **kwargs)
        self.elset = None
        self.eltype = 'B31'
        self.orientation = frame

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        # note: the string `*Element, type=B31` is generated in the part section to group elements with the same type
        return '{0}, {1}, {2}\n'.format(self.key + 1, self.nodes[0].key + 1, self.nodes[1].key + 1)


class AbaqusSpringElement(SpringElement):
    """A 1D spring element.
    """

    def __init__(self, connectivity, section, orientation=[0.0, 0.0, -1.0], thermal=None):
        super(BeamElement, self).__init__(connectivity, section, orientation, thermal)
        self._eltype = 'B31'


class AbaqusTrussElement(TrussElement):
    """A 1D element that resists axial loads.
    """
    __doc__ += TrussElement.__doc__

    def __init__(self, connectivity, section, elset=None, thermal=None):
        super(AbaqusTrussElement, self).__init__(connectivity, section, thermal)
        self.elset = elset
        self.eltype = 'T3D2'
        self.orientation = None

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        return '{0}, {1}, {2}\n'.format(self.key+1, self.connectivity[0]+1, self.connectivity[1]+1)


# ==============================================================================
# 2D elements
# ==============================================================================

class AbaqusShellElement(ShellElement):
    """A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    connectivity : list
        List containing the nodes sequence building the shell element.
    section : obj
        compas_fea2 ShellSection object
    elset : obj
        compas_fea2 Set object, optional
    thermal : bool
        NotImplemented

    """
    __doc__ += ShellElement.__doc__

    def __init__(self, connectivity, section, elset=None, thermal=None):
        super(AbaqusShellElement, self).__init__(connectivity, section, thermal)
        if not elset:
            self.elset = self.section
        else:
            self.elset = elset

        eltypes = {3: 'S3', 4: 'S4'}
        if not len(self.connectivity) in eltypes:
            raise NotImplementedError('Shells must currently have either 3 or 4 nodes')
        self._eltype = eltypes[len(self.connectivity)]

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return '{0}, {1}\n'.format(self.key+1, ','.join(str(nk+1) for nk in self.connectivity))


class AbaqusMembraneElement(MembraneElement):

    def __init__(self):
        super(AbaqusMembraneElement, self).__init__()
        raise NotImplementedError


# ==============================================================================
# 3D elements
# ==============================================================================

class AbaqusSolidElement(SolidElement):

    def __init__(self, connectivity, section, eltype=None, elset=None, thermal=None):
        super(AbaqusSolidElement, self).__init__(connectivity, section, thermal)
        if not elset:
            self.elset = self.section
        else:
            self.elset = elset

        if not eltype:
            eltypes = {4: 'C3D4', 6: 'C3D6', 8: 'C3D8', 10: 'C3D10'}
            self.eltype = eltypes[len(self.connectivity)]
        else:
            self.eltype = eltype

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return '{0}, {1}\n'.format(self.key+1, ','.join(str(node_key+1) for node_key in self.connectivity))
