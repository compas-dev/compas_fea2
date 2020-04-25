
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.utilities import cWriter

from compas_fea2.backends.abaqus.writer import Heading
from compas_fea2.backends.abaqus.writer.elements import Elements
from compas_fea2.backends.abaqus.writer.elements import Nodes
from compas_fea2.backends.abaqus.writer.sets import Sets
from compas_fea2.backends.abaqus.writer.bcs import BCs
from compas_fea2.backends.abaqus.writer.materials import Materials
from compas_fea2.backends.abaqus.writer.steps import Steps


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'Writer',
]

class Writer(cWriter, Steps, Materials, BCs, Elements, Nodes, Sets, Heading):

    """ Initialises abaqus file writer.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    def __init__(self, structure, filename, fields):
        super(Writer, self).__init__(structure, filename, fields)
        self.comment   = '**'
        self.spacer    = ', '
