
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.utilities import cWriter

from compas_fea2.backends.opensees.writer import Heading
from compas_fea2.backends.opensees.writer.elements import Elements
from compas_fea2.backends.opensees.writer.elements import Nodes
from compas_fea2.backends.opensees.writer.bcs import BCs
from compas_fea2.backends.opensees.writer.materials import Materials
from compas_fea2.backends.opensees.writer.steps import Steps


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Writer',
]

class Writer(cWriter, Steps, Materials, BCs, Elements, Nodes, Heading):

    """ Initialises base file writer.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    def __init__(self, structure, filename, fields, ndof=6):
        super(Writer, self).__init__(structure, filename, fields, ndof)
        self.comment   = '#'
        self.spacer    = ' '
