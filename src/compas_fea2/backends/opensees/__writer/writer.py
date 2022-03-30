
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.utilities import Writer

from compas_fea2.backends.opensees.__writer import Heading
from compas_fea2.backends.opensees.__writer.elements import Elements
from compas_fea2.backends.opensees.__writer.elements import Nodes
from compas_fea2.backends.opensees.__writer.bcs import BCs
from compas_fea2.backends.opensees.__writer.materials import Materials
from compas_fea2.backends.opensees.__writer.steps import Steps


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Writer',
]


class Writer(Writer, Steps, Materials, BCs, Elements, Nodes, Heading):

    """ Initialises base file writer.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    def __init__(self, structure, filename, fields, ndof=6):
        super(Writer, self).__init__(structure, filename, fields)
        self.comment = '#'
        self.spacer = ' '
        self.ndof = 6
