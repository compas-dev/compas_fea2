
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import SectionBase
from compas_fea2.model import MassSectionBase
from compas_fea2.model import AngleSectionBase
from compas_fea2.model import BoxSectionBase
from compas_fea2.model import CircularSectionBase
from compas_fea2.model import ISectionBase
from compas_fea2.model import PipeSectionBase
from compas_fea2.model import RectangularSectionBase
from compas_fea2.model import ShellSectionBase
from compas_fea2.model import MembraneSectionBase
from compas_fea2.model import SolidSectionBase
from compas_fea2.model import TrapezoidalSectionBase
from compas_fea2.model import TrussSectionBase
from compas_fea2.model import StrutSectionBase
from compas_fea2.model import TieSectionBase
from compas_fea2.model import SpringSectionBase


class RectangularSection(RectangularSectionBase):

    def __init__(self, name, b, h, material):
        super(RectangularSection, self).__init__(name, b, h, material)

    # NOTE in opensees the sectional properties are assigned directly to the element UNLESS it is a nonliner thing...in
    # that case there is a tag for the section....aaaaarrrrhhhh

    def _generate_jobdata(self):
        return f'section Elastic {self._name} {self.material._E} {self._A} {self._Iyy} {self._Ixx} {self._material.G} {self._J}'
