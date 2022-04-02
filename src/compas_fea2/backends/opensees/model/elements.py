from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import MassElement
from compas_fea2.model import BeamElement
from compas_fea2.model import TrussElement
from compas_fea2.model import ShellElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import SolidElement
from compas_fea2.model import TetrahedronElement
from compas_fea2.model import PentahedronElement
from compas_fea2.model import HexahedronElement


# ==============================================================================
# 0D elements
# ==============================================================================
class OpenseesMassElement(MassElement):
    """"""
    __doc__ += MassElement.__doc__

    def __init__(self, *, node, section, frame=None, part=None, name=None, **kwargs):
        super(OpenseesMassElement, self).__init__(nodes=[node],
                                                  section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError


# ==============================================================================
# 1D elements
# ==============================================================================

class OpenseesBeamElement(BeamElement):
    """OpenSees implementation of :class:`compas_fea2.model.BeamElement`.\n
    """
    __doc__ += BeamElement.__doc__

    def __init__(self, nodes, section, frame=[0.0, 0.0, -1.0], part=None, name=None, **kwargs):
        super(OpenseesBeamElement, self).__init__(nodes=nodes, section=section, frame=frame,
                                                  part=part, name=name, **kwargs)
        self._eltype = 'element elasticBeamColumn'

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        line = []
        line.append('geomTransf Corotational {1}\n'.format(
            self.key, ' '.join([str(i) for i in self.frame])))
        line.append('{} {} {} {} {} {} {} {} {} {} {}'.format(self._eltype,
                                                              self.key,
                                                              self.nodes[0].key,
                                                              self.nodes[1].key,
                                                              self.section.A,
                                                              self.section.material.E,
                                                              self.section.material.G,
                                                              self.section.J,
                                                              self.section.Ixx,
                                                              self.section.Iyy,
                                                              self.key))
        return ''.join(line)


class OpenseesTrussElement(TrussElement):
    """A 1D element that resists axial loads.
    """
    __doc__ += TrussElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesTrussElement, self).__init__(nodes=nodes, section=section, part=part, name=name, **kwargs)
        raise NotImplementedError()


# ==============================================================================
# 2D elements
# ==============================================================================

class OpenseesShellElement(ShellElement):
    """"""
    __doc__ += ShellElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesShellElement, self).__init__(nodes=nodes, section=section,  part=part, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesMembraneElement(MembraneElement):
    """"""
    __doc__ += MembraneElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesMembraneElement, self).__init__(nodes=nodes, section=section, part=part, name=name, **kwargs)
        raise NotImplementedError()

# ==============================================================================
# 3D elements
# ==============================================================================


class OpenseesSolidElement(SolidElement):
    """"""
    __doc__ += SolidElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesSolidElement, self).__init__(nodes=nodes, section=section,  part=part, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesTetrahedonElement(TetrahedronElement):
    """"""
    __doc__ += TetrahedronElement.__doc__

    def __init__(self, *, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesTetrahedonElement, self).__init__(nodes=nodes,
                                                        section=section, frame=None, part=part, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesPentahedronElement(PentahedronElement):
    """"""
    __doc__ += PentahedronElement.__doc__

    def __init__(self, *, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesPentahedronElement, self).__init__(nodes=nodes,
                                                         section=section, frame=None, part=part, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesHexahedronElement(HexahedronElement):
    """"""
    __doc__ += HexahedronElement.__doc__

    def __init__(self, *, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesHexahedronElement, self).__init__(nodes=nodes,
                                                        section=section, frame=None, part=part, name=name, **kwargs)
        raise NotImplementedError()
