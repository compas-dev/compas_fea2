from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.elements import BeamElement
from compas_fea2.model.elements import Face
from compas_fea2.model.elements import HexahedronElement
from compas_fea2.model.elements import MassElement
from compas_fea2.model.elements import MembraneElement
from compas_fea2.model.elements import PentahedronElement
from compas_fea2.model.elements import ShellElement
from compas_fea2.model.elements import SpringElement
from compas_fea2.model.elements import StrutElement
from compas_fea2.model.elements import TetrahedronElement
from compas_fea2.model.elements import TieElement
from compas_fea2.model.elements import TrussElement

class SofistikBeamElement(BeamElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.BeamElement`.\n
    """
    __doc__ += BeamElement.__doc__

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(SofistikBeamElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, name=name, **kwargs)


    def _generate_jobdata(self):
        return "BEAM NO {} NA {} NE {} NCS {} DIV 1".format(self.key+1, self.nodes[0].key+1, self.nodes[1].key+1, self.section.key+1)

class SofistikFace(Face):
    """Sofistik implementation of :class:`compas_fea2.model.elements.Face`.\n
    """
    __doc__ += Face.__doc__

    def __init__(self, *, nodes, tag, element=None, name=None):
        super(SofistikFace, self).__init__(nodes=nodes, tag=tag, element=element, name=name)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikHexahedronElement(HexahedronElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.HexahedronElement`.\n
    """
    __doc__ += HexahedronElement.__doc__

    def __init__(self, *, nodes, section, implementation=None, name=None, **kwargs):
        super(SofistikHexahedronElement, self).__init__(nodes=nodes, section=section, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikMassElement(MassElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.MassElement`.\n
    """
    __doc__ += MassElement.__doc__

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(SofistikMassElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikMembraneElement(MembraneElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.MembraneElement`.\n
    """
    __doc__ += MembraneElement.__doc__

    def __init__(self, *, nodes, frame, section=None, implementation=None, rigid=False, name=None, **kwargs):
        super(SofistikMembraneElement, self).__init__(nodes=nodes, frame=frame, section=section, implementation=implementation, rigid=rigid, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikPentahedronElement(PentahedronElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.PentahedronElement`.\n
    """
    __doc__ += PentahedronElement.__doc__

    def __init__(self, *, nodes, section, implementation=None, name=None, **kwargs):
        super(SofistikPentahedronElement, self).__init__(nodes=nodes, section=section, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikShellElement(ShellElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.ShellElement`.\n
    """
    __doc__ += ShellElement.__doc__

    def __init__(self, *, nodes, frame=None, section=None, implementation=None, rigid=False, name=None, **kwargs):
        super(SofistikShellElement, self).__init__(nodes=nodes, frame=frame, section=section, implementation=implementation, rigid=rigid, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikSpringElement(SpringElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.SpringElement`.\n
    """
    __doc__ += SpringElement.__doc__

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(SofistikSpringElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikStrutElement(StrutElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.StrutElement`.\n
    """
    __doc__ += StrutElement.__doc__

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(SofistikStrutElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTetrahedronElement(TetrahedronElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.TetrahedronElement`.\n
    """
    __doc__ += TetrahedronElement.__doc__

    def __init__(self, *, nodes, section, implementation=None, name=None, **kwargs):
        super(SofistikTetrahedronElement, self).__init__(nodes=nodes, section=section, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTieElement(TieElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.TieElement`.\n
    """
    __doc__ += TieElement.__doc__

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(SofistikTieElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTrussElement(TrussElement):
    """Sofistik implementation of :class:`compas_fea2.model.elements.TrussElement`.\n
    """
    __doc__ += TrussElement.__doc__

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(SofistikTrussElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

