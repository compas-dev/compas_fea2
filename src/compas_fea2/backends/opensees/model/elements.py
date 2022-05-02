from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import MassElement
from compas_fea2.model import BeamElement
from compas_fea2.model import TrussElement
from compas_fea2.model import ShellElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import SolidElement


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

    def __init__(self, nodes, section, implementation='elasticBeamColumn', frame=[0.0, 0.0, -1.0], part=None, name=None, **kwargs):
        super(OpenseesBeamElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation,
                                                  part=part, name=name, **kwargs)

        self._implementation = BeamElement.from_name(implementation)

        try:
            self._job_data = getattr(self, implementation)
        except:
            raise ValueError('{} is not a valid implementation model'.format(implementation))

    def _generate_jobdata(self):
        return '\n'.join(['geomTransf Corotational {1}'.format(self.key, ' '.join([str(i) for i in self.frame])),
                          self._job_data
                          ])

    def _elasticBeamColumn(self):
        """Construct an elasticBeamColumn element object.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/gradientInelasticBeamColumn.html>`_
        """
        return 'element {} {} {} {} {} {} {} {} {}'.format(self._implementation,
                                                           self.key,
                                                           ' '.join(node.key for node in self.nodes),
                                                           self.section.A,
                                                           self.section.material.E,
                                                           self.section.material.G,
                                                           self.section.J,
                                                           self.section.Ixx,
                                                           self.section.Iyy,
                                                           self.key)

    def _inelasticBeamColum(self):
        raise NotImplementedError('Currently under development')
        return 'element  {} {} {} $numIntgrPts $endSecTag1 $intSecTag $endSecTag2 $lambda1 $lambda2 $lc $transfTag <-integration integrType> <-iter $maxIter $minTol $maxTol>'. format(self._implementation,
                                                                                                                                                                                       self._key,
                                                                                                                                                                                       ' '.join(node.key for node in self.nodes))


class OpenseesTrussElement(TrussElement):
    """A 1D element that resists axial loads.
    """
    __doc__ += TrussElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesTrussElement, self).__init__(nodes=nodes, section=section, part=part, name=name, **kwargs)
        raise NotImplementedError


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
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    """
    # TODO maybe move mat_behavior to the material or section

    def __init__(self, nodes, section, implementation, mat_behaviour='PlainStess', part=None, name=None, **kwargs):
        super(OpenseesShellElement, self).__init__(nodes=nodes, section=section,
                                                   part=part, implementation=implementation, name=name, **kwargs)
        if self._nodes != 4:
            raise NotImplementedError('Shell elements in Opensees can only have 4 nodes.')
        self._mat_behaviour = mat_behaviour
        self._job_data = None

    @property
    def mat_behaviour(self):
        return self._mat_behaviour

    def _generate_jobdata(self):
        try:
            return getattr(self, '_'+self._implementation.lower())()
        except:
            raise ValueError('{} is not a valid implementation.'.format(self._implementation))

    def _asdshellq4(self):
        """Construct an ASDShellQ4 element object.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDShellQ4.html>`_
        """
        return 'element ASDShellQ4  {}  {}'.format(self.key,
                                                   ' '.join(node.key for node in self.nodes),
                                                   self.section.key)

    def _fournodequad(self):
        """Construct a FourNodeQuad element object which uses a bilinear isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/Quad.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return 'element quad {} {} {} {}'.format(self.key,
                                                 ' '.join(node.key for node in self.nodes),
                                                 self.section.thickness,
                                                 self.mat_behaviour,
                                                 self.section.material.key)

    def _sspquad(self):
        """Construct a SSPquad (SSP –> Stabilized Single Point) element.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SSPquad.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return 'element SSPquad {} {} {} {}'.format(self.key,
                                                    ' '.join(node.key for node in self.nodes),
                                                    self.section.material.key,
                                                    self.section.material.key,
                                                    self.mat_behaviour,
                                                    self.section.thickness)


class OpenseesMembraneElement(MembraneElement):
    """"""
    __doc__ += MembraneElement.__doc__

    def __init__(self, nodes, section, part=None, name=None, **kwargs):
        super(OpenseesMembraneElement, self).__init__(nodes=nodes, section=section, part=part, name=name, **kwargs)
        raise NotImplementedError

# ==============================================================================
# 3D elements
# ==============================================================================


class OpenseesSolidElement(SolidElement):
    """"""
    __doc__ += SolidElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    """

    def __init__(self, nodes, section, implementation='stdBrick', part=None, name=None, **kwargs):
        super(OpenseesSolidElement, self).__init__(nodes=nodes, section=section,
                                                   part=part, implementation=implementation, name=name, **kwargs)

    def _get_implementation(self):
        try:
            return getattr(self, '_'+self._type.lower())
        except:
            raise ValueError('{} is not a valid implementation.'.format(self._implementation))

    def _generate_jobdata(self):
        return 'element {}  {}  {}'.format(self.key,
                                           self._implementation,
                                           ' '.join(node.key for node in self.nodes),
                                           self.section.material.key)

    # TODO complete implementations: for now it is all done in _generate_jobdata
    def _stdbrick(self):
        """Construct an eight-node brick element object, which uses the standard isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/stdBrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return

    def _bbarbrick(self):
        """Construct an eight-node mixed volume/pressure brick element object, which uses a trilinear isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/bbarBrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return

    def _sspbrick(self):
        """Construct an eight-node ssp brick element. The SSPbrick element is an
        eight-node hexahedral element using physically stabilized single-point
        integration (SSP –> Stabilized Single Point).

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SSPbrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """

        return
