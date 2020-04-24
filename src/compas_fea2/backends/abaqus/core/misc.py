
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2._core import cMisc
from compas_fea2._core import cAmplitude
from compas_fea2._core import cTemperatures

# Author(s): Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'Misc',
    'Amplitude',
    'Temperatures'
]


class Misc(cMisc):

    """ Initialises base Misc object.

    Parameters
    ----------
    name : str
        Misc object name.

    Returns
    -------
    None

    """

    def __init__(self, name):
        super(Misc, self).__init__(name)


class Amplitude(cAmplitude):

    """ Initialises an Amplitude object to act as a discretised function f(x).

    Parameters
    ----------
    name : str
        Amplitude object name.
    values : list
        Amplitude function value pairs [[x0, y0], [x1, y1], ..].

    Returns
    -------
    None

    """

    def __init__(self, name, values):
        super(Amplitude, self).__init__(name, values)


class Temperatures(cTemperatures):

    """ Define nodal temperatures data.

    Parameters
    ----------
    name : str
        Temperature object name.
    file : str
        Path of nodal temperatures file to extract data from.
    values : list
        List of [[node, temperature, time], ...] data.
    tend : float
        End time in seconds to read data till.

    Returns
    -------
    None

    """

    def __init__(self, name, file, values, tend):
        super(Temperatures, self).__init__(name, file, values, tend)
