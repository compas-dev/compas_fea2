from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.elements import BeamElement
from compas_fea2.model.elements import HexahedronElement
from compas_fea2.model.elements import MassElement
from compas_fea2.model.elements import MembraneElement
from compas_fea2.model.elements import PentahedronElement
from compas_fea2.model.elements import ShellElement
from compas_fea2.model.elements import SolidElement
from compas_fea2.model.elements import SpringElement
from compas_fea2.model.elements import StrutElement
from compas_fea2.model.elements import TetrahedronElement
from compas_fea2.model.elements import TieElement
from compas_fea2.model.elements import TrussElement


class AnsysBeamElement(BeamElement):
    """ Ansys implementation of :class:`.BeamElement`.\n
    """
    __doc__ += BeamElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysBeamElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysHexahedronElement(HexahedronElement):
    """ Ansys implementation of :class:`.HexahedronElement`.\n
    """
    __doc__ += HexahedronElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysHexahedronElement, self).__init__(nodes=nodes,
                                                     section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysMassElement(MassElement):
    """ Ansys implementation of :class:`.MassElement`.\n
    """
    __doc__ += MassElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysMassElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysMembraneElement(MembraneElement):
    """ Ansys implementation of :class:`.MembraneElement`.\n
    """
    __doc__ += MembraneElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysMembraneElement, self).__init__(nodes=nodes,
                                                   section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysPentahedronElement(PentahedronElement):
    """ Ansys implementation of :class:`.PentahedronElement`.\n
    """
    __doc__ += PentahedronElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysPentahedronElement, self).__init__(nodes=nodes,
                                                      section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysShellElement(ShellElement):
    """ Ansys implementation of :class:`.ShellElement`.\n
    """
    __doc__ += ShellElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysShellElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysSolidElement(SolidElement):
    """ Ansys implementation of :class:`.SolidElement`.\n
    """
    __doc__ += SolidElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysSolidElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysSpringElement(SpringElement):
    """ Ansys implementation of :class:`.SpringElement`.\n
    """
    __doc__ += SpringElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysSpringElement, self).__init__(nodes=nodes,
                                                 section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysStrutElement(StrutElement):
    """ Ansys implementation of :class:`.StrutElement`.\n
    """
    __doc__ += StrutElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysStrutElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysTetrahedronElement(TetrahedronElement):
    """ Ansys implementation of :class:`.TetrahedronElement`.\n
    """
    __doc__ += TetrahedronElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysTetrahedronElement, self).__init__(nodes=nodes,
                                                      section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysTieElement(TieElement):
    """ Ansys implementation of :class:`.TieElement`.\n
    """
    __doc__ += TieElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysTieElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysTrussElement(TrussElement):
    """ Ansys implementation of :class:`.TrussElement`.\n
    """
    __doc__ += TrussElement.__doc__

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(AnsysTrussElement, self).__init__(nodes=nodes, section=section, frame=frame, part=part, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
