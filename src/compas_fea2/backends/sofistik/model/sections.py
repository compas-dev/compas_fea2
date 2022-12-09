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

class SofistikAngleSection(AngleSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.AngleSection`.\n 
    """
    __doc__ += AngleSection.__doc__

    def __init__(self, w, h, t, material, name=None, **kwargs):
        super(SofistikAngleSection, self).__init__(w=w, h=h, t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikBeamSection(BeamSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.BeamSection`.\n
    """
    __doc__ += BeamSection.__doc__

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, name=None, **kwargs):
        super(SofistikBeamSection, self).__init__(A=A, Ixx=Ixx, Iyy=Iyy, Ixy=Ixy, Avx=Avx, Avy=Avy, J=J, g0=g0, gw=gw, material=material, name=name, **kwargs)
        

    def _generate_jobdata(self):
        return "SVAL no {} mno {} a {} iz {} iy {} iyz {} az {} ay {} it {} g0? {} gw? {}".format(self.key+1,
                                                                                self.material.key+1,
                                                                                self.A,
                                                                                self.Ixx,
                                                                                self.Iyy,
                                                                                self.Ixy,
                                                                                self.Avx,
                                                                                self.Avy,
                                                                                self.J,
                                                                                self.g0,
                                                                                self.gw)

class SofistikBoxSection(BoxSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.BoxSection`.\n
    """
    __doc__ += BoxSection.__doc__

    def __init__(self, w, h, tw, tf, material, name=None, **kwargs):
        super(SofistikBoxSection, self).__init__(w=w, h=h, tw=tw, tf=tf, material=material, name=name, **kwargs)
        #NEED TO FIND IN THE SREC COMMAND IN SOFISTIK THE EQUIVALENT OF tw AND tf

    def _generate_jobdata(self):
        return "SREC no {}  h {}  b {} mno {} ToFindEquivalentOftw {} ToFindEquivalentOftf {}".format(self.key+1, self.h, self.w, self.material.key+1, self.tw, self.tf)

class SofistikCircularSection(CircularSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.CircularSection`.\n
    """
    __doc__ += CircularSection.__doc__

    def __init__(self, r, material, name=None, **kwargs):
        super(SofistikCircularSection, self).__init__(r=r, material=material, name=name, **kwargs)
        

    def _generate_jobdata(self):
        return "CIRC no {}  r {}  mno {}".format(self.key+1, self.r, self.material.key+1)

class SofistikHexSection(HexSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.HexSection`.\n
    """
    __doc__ += HexSection.__doc__

    def __init__(self, r, t, material, name=None, **kwargs):
        super(SofistikHexSection, self).__init__(r=r, t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikISection(ISection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.ISection`.\n
    """
    __doc__ += ISection.__doc__

    def __init__(self, w, h, tw, tf, material, name=None, **kwargs):
        super(SofistikISection, self).__init__(w=w, h=h, tw=tw, tf=tf, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikMassSection(MassSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.MassSection`.\n
    """
    __doc__ += MassSection.__doc__

    def __init__(self, mass, name=None, **kwargs):
        super(SofistikMassSection, self).__init__(mass=mass, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikMembraneSection(MembraneSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.MembraneSection`.\n
    """
    __doc__ += MembraneSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(SofistikMembraneSection, self).__init__(t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikPipeSection(PipeSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.PipeSection`.\n
    """
    __doc__ += PipeSection.__doc__

    def __init__(self, r, t, material, name=None, **kwargs):
        super(SofistikPipeSection, self).__init__(r=r, t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikRectangularSection(RectangularSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.RectangularSection`.\n
    """
    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, name=None, **kwargs):
        super(SofistikRectangularSection, self).__init__(w=w, h=h, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikShellSection(ShellSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.ShellSection`.\n
    """
    __doc__ += ShellSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(SofistikShellSection, self).__init__(t=t, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikSolidSection(SolidSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.SolidSection`.\n
    """
    __doc__ += SolidSection.__doc__

    def __init__(self, material, name=None, **kwargs):
        super(SofistikSolidSection, self).__init__(material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikSpringSection(SpringSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.SpringSection`.\n
    """
    __doc__ += SpringSection.__doc__

    def __init__(self, forces=None, displacements=None, stiffness=None, name=None, **kwargs):
        super(SofistikSpringSection, self).__init__(forces=forces, displacements=displacements, stiffness=stiffness, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikStrutSection(StrutSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.StrutSection`.\n
    """
    __doc__ += StrutSection.__doc__

    def __init__(self, A, material, name=None, **kwargs):
        super(SofistikStrutSection, self).__init__(A=A, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTieSection(TieSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.TieSection`.\n
    """
    __doc__ += TieSection.__doc__

    def __init__(self, A, material, name=None, **kwargs):
        super(SofistikTieSection, self).__init__(A=A, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTrapezoidalSection(TrapezoidalSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.TrapezoidalSection`.\n
    """
    __doc__ += TrapezoidalSection.__doc__

    def __init__(self, w1, w2, h, material, name=None, **kwargs):
        super(SofistikTrapezoidalSection, self).__init__(w1=w1, w2=w2, h=h, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTrussSection(TrussSection):
    """Sofistik implementation of :class:`compas_fea2.model.sections.TrussSection`.\n
    """
    __doc__ += TrussSection.__doc__

    def __init__(self, A, material, name=None, **kwargs):
        super(SofistikTrussSection, self).__init__(A=A, material=material, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

