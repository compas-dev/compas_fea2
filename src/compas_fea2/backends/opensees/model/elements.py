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

    def __init__(self, nodes, section, eltype=None, frame=[0.0, 0.0, -1.0], part=None, name=None, **kwargs):
        super(OpenseesBeamElement, self).__init__(nodes=nodes, section=section, frame=frame,
                                                  part=part, name=name, **kwargs)
        self._eltype = eltype

    @property
    def eltype(self):
        return self._eltype

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
        line.append('geomTransf Corotational {1}\n'.format(self.key, ' '.join([str(i) for i in self.frame])))

        elements_formulations = {
            'elasticBeamColumn': 'element {} {} {} {} {} {} {} {} {}'.format(self._eltype,
                                                                             self.key,
                                                                             ' '.join(node.key for node in self.nodes),
                                                                             self.section.A,
                                                                             self.section.material.E,
                                                                             self.section.material.G,
                                                                             self.section.J,
                                                                             self.section.Ixx,
                                                                             self.section.Iyy,
                                                                             self.key),
            'gradientInelasticBeamColumn': 'element  {} {} {} $numIntgrPts $endSecTag1 $intSecTag $endSecTag2 $lambda1 $lambda2 $lc $transfTag <-integration integrType> <-iter $maxIter $minTol $maxTol>'. format(self._eltype,
                                                                                                                                                                                                                   self._key,
                                                                                                                                                                                                                   ' '.join(node.key for node in self.nodes))}

        line.append(elements_formulations[self._eltype])
        return ''.join(line)

    @staticmethod
    def elasticBeamColumn(nodes, section, frame=[0.0, 0.0, -1.0], part=None, name=None, **kwargs):
        """Construct an elasticBeamColumn element object.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/gradientInelasticBeamColumn.html>`_
        """
        return OpenseesBeamElement(nnodes=nodes, section=section, eltype='elasticBeamColumn', frame=frame, part=part, name=name, **kwargs)

    @staticmethod
    def inelasticBeamColumn(nodes, section, frame=[0.0, 0.0, -1.0], part=None, name=None, **kwargs):
        """Construct a gradientInelasticBeamColumn element object, which is based
        on a force/flexibility-based (FB) gradient inelastic (GI) element
        formulation with an iterative solution algorithm.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/gradientInelasticBeamColumn.html>`_
        """
        raise NotImplementedError('Currently under development')
        return OpenseesBeamElement(nnodes=nodes, section=section, eltype='gradientInelasticBeamColumn', frame=frame, part=part, name=name, **kwargs)


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
    """OpenSees implementation of a :class:`ShellElemnt`.

    """
    __doc__ += ShellElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    eltype : str
        Element type formulation.
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    Addtional Attributes
    --------------------
    eltype : str
        Element type formulation.
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    """
    # TODO maybe move mat_behavior to the material or section

    def __init__(self, nodes, section, eltype, mat_behaviour=None, part=None, name=None, **kwargs):
        super(OpenseesShellElement, self).__init__(nodes=nodes, section=section,  part=part, name=name, **kwargs)
        if self._nodes != 4:
            raise NotImplementedError('Shell elements in Opensees can only have 4 nodes.')
        self._eltype = eltype
        self._mat_behaviour = mat_behaviour

    @property
    def eltype(self):
        return self._eltype

    @property
    def mat_behaviour(self):
        return self._mat_behaviour

    @staticmethod
    def ASDShellQ4(nodes, section, part=None, name=None, **kwargs):
        """Construct an ASDShellQ4 element object.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDShellQ4.html>`_
        """
        return OpenseesShellElement(nodes, section, 'ASDShellQ4', mat_behaviour=None, part=None, name=None, **kwargs)

    @staticmethod
    def FourNodeQuad(nodes, section, part=None, name=None, mat_behavior='PlainStess', **kwargs):
        """Construct a FourNodeQuad element object which uses a bilinear isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/Quad.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return OpenseesShellElement(nodes, section, 'FourNodeQuad', mat_behaviour=mat_behavior, part=None, name=None, **kwargs)

    @staticmethod
    def SSPQuad(nodes, section, part=None, name=None, mat_behavior='PlainStess', **kwargs):
        """Construct a SSPquad (SSP –> Stabilized Single Point) element.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SSPquad.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return OpenseesShellElement(nodes, section, 'SSPQuad', mat_behaviour=None, part=None, name=None, **kwargs)

    def _generate_jobdata(self):
        elements_formulations = {
            'ASDShellQ4': 'element ASDShellQ4  {}  {}'.format(self.key,
                                                              ' '.join(node.key for node in self.nodes),
                                                              self.section.key),
            'FourNodeQuad': 'element quad {} {} {} {}'.format(self.key,
                                                              ' '.join(node.key for node in self.nodes),
                                                              self.section.thickness,
                                                              self.mat_behaviour,
                                                              self.section.material.key),
            'SSPQuad': 'element SSPquad {} {} {} {}'.format(self.key,
                                                            ' '.join(node.key for node in self.nodes),
                                                            self.section.material.key,
                                                            self.section.material.key,
                                                            self.mat_behaviour,
                                                            self.section.thickness)
        }
        return elements_formulations[self._eltype]


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
    __doc__ += """
    Additional Parameters
    ---------------------
    eltype : str
        Element type formulation.
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    Addtional Attributes
    --------------------
    eltype : str
        Element type formulation.
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    """

    def __init__(self, nodes, section, eltype=None, part=None, name=None, **kwargs):
        super(OpenseesSolidElement, self).__init__(nodes=nodes, section=section,  part=part, name=name, **kwargs)
        self._eltype = eltype

    @property
    def eltype(self):
        return self._eltype

    @staticmethod
    def stdBrick(nodes, section, part=None, name=None, **kwargs):
        """Construct an eight-node brick element object, which uses the standard isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/stdBrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return OpenseesSolidElement(nodes, section, eltype='stdBrick', part=part, name=name, **kwargs)

    @staticmethod
    def bbarBrick(nodes, section, part=None, name=None, **kwargs):
        """Construct an eight-node mixed volume/pressure brick element object, which uses a trilinear isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/bbarBrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return OpenseesSolidElement(nodes, section, eltype='stdBrick', part=part, name=name, **kwargs)

    @staticmethod
    def SSPbrick(nodes, section, part=None, name=None, **kwargs):
        """Construct an eight-node ssp brick element. The SSPbrick element is an
        eight-node hexahedral element using physically stabilized single-point
        integration (SSP –> Stabilized Single Point).

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SSPbrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return OpenseesSolidElement(nodes, section, eltype='stdBrick', part=part, name=name, **kwargs)

    def _generate_jobdata(self):
        return 'element {}  {}  {}'.format(self.key,
                                           self._eltype,
                                           ' '.join(node.key for node in self.nodes),
                                           self.section.material.key)


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
