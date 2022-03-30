
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import _Section
from compas_fea2.model import MassSection
from compas_fea2.model import AngleSection
from compas_fea2.model import BoxSection
from compas_fea2.model import CircularSection
from compas_fea2.model import ISection
from compas_fea2.model import PipeSection
from compas_fea2.model import RectangularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import MembraneSection
from compas_fea2.model import SolidSection
from compas_fea2.model import TrapezoidalSection
from compas_fea2.model import TrussSection
from compas_fea2.model import StrutSection
from compas_fea2.model import TieSection
from compas_fea2.model import SpringSection


class OpenseesRectangularSection(RectangularSection):
    """OpenSees implementation of :class:`RectangularSection`. \n
    """
    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, name=None, **kwargs):
        super(OpenseesRectangularSection, self).__init__(w, h, material, name=None, **kwargs)

    # NOTE in opensees the sectional properties are assigned directly to the element UNLESS it is a nonliner thing...
    # in that case there is a tag for the section....aaaaarrrrhhhh

    def _generate_jobdata(self):
        return f'section Elastic {self.name} {self.material.E} {self.A} {self.Iyy} {self.Ixx} {self.material.G} {self.J}'
