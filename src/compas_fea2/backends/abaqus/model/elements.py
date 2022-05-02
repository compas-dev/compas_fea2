from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import MassElement
from compas_fea2.model import BeamElement
from compas_fea2.model import TrussElement
from compas_fea2.model import ShellElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import SolidElement


def _generate_jobdata(element):
    """Generates the common string information for the input file of all the
    elements.

    Note
    ----
    the string portion `*Element, type=___` is generated in the part section
    to group elements with the same type.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).

    """
    return '{0}, {1}\n'.format(element.key+1, ','.join(str(node.key+1) for node in element.nodes))


# ==============================================================================
# 0D elements
# ==============================================================================
class AbaqusMassElement(MassElement):
    """Abaqus implementation of :class:`MassElement`\n"""
    __doc__ += MassElement.__doc__

    def __init__(self, *, node, section, frame=None, part=None, name=None, **kwargs):
        super(AbaqusMassElement, self).__init__(nodes=[node],
                                                section=section, frame=frame, part=part, name=name, **kwargs)

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
    """Abaqus implementation of :class:`BeamElement`\n"""
    __doc__ += BeamElement.__doc__

    def __init__(self, nodes, section, frame=[0.0, 0.0, -1.0], part=None, name=None, **kwargs):
        super(AbaqusBeamElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        self._elset = None
        self._implementation = 'B31'
        self._orientation = frame

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class AbaqusTrussElement(TrussElement):
    """Abaqus implementation of :class:`TrussElement`\n"""
    __doc__ += TrussElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(AbaqusTrussElement, self).__init__(nodes=nodes, section=section, part=part, name=name, **kwargs)
        self._elset = None
        self._implementation = 'T3D2'
        self._orientation = None

    def _generate_jobdata(self):
        return _generate_jobdata(self)

# ==============================================================================
# 2D elements
# ==============================================================================


class AbaqusShellElement(ShellElement):
    """Abaqus implementation of :class:`ShellElement`\n"""
    __doc__ += ShellElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.

    """

    def __init__(self, nodes, section, part=None, reduced=False, name=None, **kwargs):
        super(AbaqusShellElement, self).__init__(nodes=nodes, section=section,  part=part, name=name, **kwargs)
        self._reduced = reduced
        self._elset = None
        implementations = {3: 'S3', 4: 'S4'}
        if not len(self.nodes) in implementations:
            raise NotImplementedError('Shells must currently have either 3 or 4 nodes')
        self._implementation = implementations[len(self.nodes)]
        if self._reduced:
            self._implementation += 'R'

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class AbaqusMembraneElement(MembraneElement):
    """Abaqus implementation of :class:`MembraneElement`\n"""
    __doc__ += MembraneElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.

    """

    def __init__(self, nodes, section, part=None, reduced=False, name=None, **kwargs):
        super(AbaqusMembraneElement, self).__init__(nodes=nodes, section=section, part=part, name=name, **kwargs)
        self._elset = None
        self._reduced = reduced
        implementations = {3: 'M3D3', 4: 'M3D4'}
        if not len(self.nodes) in implementations:
            raise NotImplementedError('Membrane elements must currently have either 3 or 4 nodes')
        self._implementation = implementations[len(self.nodes)]
        if self._reduced and len(self.nodes) > 3:
            self._implementation += 'R'

    def _generate_jobdata(self):
        return _generate_jobdata(self)

# ==============================================================================
# 3D elements
# ==============================================================================


class AbaqusSolidElement(SolidElement):
    """Abaqus implementation of :class:`SolidElement`\n"""
    __doc__ += SolidElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.

    """

    def __init__(self, nodes, section, part=None, implementation='C3D4', reduced=False, name=None, **kwargs):
        super(AbaqusSolidElement, self).__init__(nodes=nodes, section=section,
                                                 part=part, implementation=implementation, name=name, **kwargs)
        self._reduced = reduced
        if self._reduced:
            self._implementation += 'R'

    def _check_implementation(self, n_nodes):
        if len(self.nodes) != n_nodes:
            raise ValueError('{} must have {} nodes'.fromat(self.implementation, len(self.nodes)))

    def _generate_jobdata(self):
        raise NotImplementedError('You must select a element type implementation')


class _C3D4(AbaqusSolidElement):
    def __init__(self, nodes, section, part=None, reduced=False, name=None, **kwargs):
        super(_C3D4, self).__init__(nodes=nodes, section=section,
                                    implementation='C3D4', part=part, reduced=reduced, name=name, **kwargs)
        self._check_implementation(4)

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class _C3D6(AbaqusSolidElement):
    def __init__(self, nodes, section, part=None, reduced=False, name=None, **kwargs):
        super(_C3D6, self).__init__(nodes=nodes, section=section,
                                    implementation='C3D6', part=part, reduced=reduced, name=name, **kwargs)
        self._check_implementation(6)

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class _C3D8(AbaqusSolidElement):
    def __init__(self, nodes, section, part=None, reduced=False, name=None, **kwargs):
        super(_C3D8, self).__init__(nodes=nodes, section=section,
                                    implementation='C3D8', part=part, reduced=reduced, name=name, **kwargs)
        self._check_implementation(8)

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class _C3D10(AbaqusSolidElement):
    def __init__(self, nodes, section, part=None, reduced=False, name=None, **kwargs):
        super(_C3D10, self).__init__(nodes=nodes, section=section,
                                     implementation='C3D10', part=part, reduced=reduced, name=name, **kwargs)
        self._check_implementation(10)

    def _generate_jobdata(self):
        return _generate_jobdata(self)
