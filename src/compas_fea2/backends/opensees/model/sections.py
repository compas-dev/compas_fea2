
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Section
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


class RectangularSection(RectangularSection):
    """OpenSees implementation of :class:`RectangularSection`. \n
    """
    __doc__ += RectangularSection.__doc__

    def __init__(self, name, b, h, material):
        super(RectangularSection, self).__init__(name, b, h, material)

    # NOTE in opensees the sectional properties are assigned directly to the element UNLESS it is a nonliner thing...in
    # that case there is a tag for the section....aaaaarrrrhhhh

    def _generate_jobdata(self):
        return f'section Elastic {self._name} {self.material._E} {self._A} {self._Iyy} {self._Ixx} {self._material.G} {self._J}'
