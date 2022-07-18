from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.sections import AngleSection
from compas_fea2.model.sections import BeamSection
from compas_fea2.model.sections import BoxSection
from compas_fea2.model.sections import CircularSection
from compas_fea2.model.sections import HexSection
from compas_fea2.model.sections import ISection
from compas_fea2.model.sections import MassSection
from compas_fea2.model.sections import MembraneSection
from compas_fea2.model.sections import PipeSection
from compas_fea2.model.sections import RectangularSection
from compas_fea2.model.sections import ShellSection
from compas_fea2.model.sections import SolidSection
from compas_fea2.model.sections import SpringSection
from compas_fea2.model.sections import StrutSection
from compas_fea2.model.sections import TieSection
from compas_fea2.model.sections import TrapezoidalSection
from compas_fea2.model.sections import TrussSection

class AnsysAngleSection(AngleSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.AngleSection`.\n
    """
    __doc__ += AngleSection.__doc__

    def __init__(self, w, h, t, material, name=None, **kwargs):
        super(AnsysAngleSection, self).__init__(w=w, h=h, t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysBeamSection(BeamSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.BeamSection`.\n
    """
    __doc__ += BeamSection.__doc__

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, name=None, **kwargs):
        super(AnsysBeamSection, self).__init__(A=A, Ixx=Ixx, Iyy=Iyy, Ixy=Ixy, Avx=Avx, Avy=Avy, J=J, g0=g0, gw=gw, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysBoxSection(BoxSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.BoxSection`.\n
    """
    __doc__ += BoxSection.__doc__

    def __init__(self, w, h, tw, tf, material, name=None, **kwargs):
        super(AnsysBoxSection, self).__init__(w=w, h=h, tw=tw, tf=tf, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysCircularSection(CircularSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.CircularSection`.\n
    """
    __doc__ += CircularSection.__doc__

    def __init__(self, r, material, name=None, **kwargs):
        super(AnsysCircularSection, self).__init__(r=r, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysHexSection(HexSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.HexSection`.\n
    """
    __doc__ += HexSection.__doc__

    def __init__(self, r, t, material, name=None, **kwargs):
        super(AnsysHexSection, self).__init__(r=r, t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysISection(ISection):
    """Ansys implementation of :class:`compas_fea2.model.sections.ISection`.\n
    """
    __doc__ += ISection.__doc__

    def __init__(self, w, h, tw, tf, material, name=None, **kwargs):
        super(AnsysISection, self).__init__(w=w, h=h, tw=tw, tf=tf, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysMassSection(MassSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.MassSection`.\n
    """
    __doc__ += MassSection.__doc__

    def __init__(self, mass, name=None, **kwargs):
        super(AnsysMassSection, self).__init__(mass=mass, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysMembraneSection(MembraneSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.MembraneSection`.\n
    """
    __doc__ += MembraneSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(AnsysMembraneSection, self).__init__(t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysPipeSection(PipeSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.PipeSection`.\n
    """
    __doc__ += PipeSection.__doc__

    def __init__(self, r, t, material, name=None, **kwargs):
        super(AnsysPipeSection, self).__init__(r=r, t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysRectangularSection(RectangularSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.RectangularSection`.\n
    """
    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, name=None, **kwargs):
        super(AnsysRectangularSection, self).__init__(w=w, h=h, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysShellSection(ShellSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.ShellSection`.\n
    """
    __doc__ += ShellSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(AnsysShellSection, self).__init__(t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysSolidSection(SolidSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.SolidSection`.\n
    """
    __doc__ += SolidSection.__doc__

    def __init__(self, material, name=None, **kwargs):
        super(AnsysSolidSection, self).__init__(material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysSpringSection(SpringSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.SpringSection`.\n
    """
    __doc__ += SpringSection.__doc__

    def __init__(self, forces=None, displacements=None, stiffness=None, name=None, **kwargs):
        super(AnsysSpringSection, self).__init__(forces=forces, displacements=displacements, stiffness=stiffness, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysStrutSection(StrutSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.StrutSection`.\n
    """
    __doc__ += StrutSection.__doc__

    def __init__(self, A, material, name=None, **kwargs):
        super(AnsysStrutSection, self).__init__(A=A, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysTieSection(TieSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.TieSection`.\n
    """
    __doc__ += TieSection.__doc__

    def __init__(self, A, material, name=None, **kwargs):
        super(AnsysTieSection, self).__init__(A=A, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysTrapezoidalSection(TrapezoidalSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.TrapezoidalSection`.\n
    """
    __doc__ += TrapezoidalSection.__doc__

    def __init__(self, w1, w2, h, material, name=None, **kwargs):
        super(AnsysTrapezoidalSection, self).__init__(w1=w1, w2=w2, h=h, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysTrussSection(TrussSection):
    """Ansys implementation of :class:`compas_fea2.model.sections.TrussSection`.\n
    """
    __doc__ += TrussSection.__doc__

    def __init__(self, A, material, name=None, **kwargs):
        super(AnsysTrussSection, self).__init__(A=A, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

