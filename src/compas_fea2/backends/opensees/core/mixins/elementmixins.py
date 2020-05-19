
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2._core.mixins.elementmixins import cElementMixins

# from compas_fea2.backends.opensees.core.elements import *


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'ElementMixins',
]


# func_dict = {
#     'BeamElement':        BeamElement,
#     'SpringElement':      SpringElement,
#     'TrussElement':       TrussElement,
#     'StrutElement':       StrutElement,
#     'TieElement':         TieElement,
#     'ShellElement':       ShellElement,
#     'MembraneElement':    MembraneElement,
#     'FaceElement':        FaceElement,
#     'SolidElement':       SolidElement,
#     'TetrahedronElement': TetrahedronElement,
#     'PentahedronElement': PentahedronElement,
#     'HexahedronElement':  HexahedronElement,
#     'MassElement':        MassElement
# }


class ElementMixins(cElementMixins):
    pass
