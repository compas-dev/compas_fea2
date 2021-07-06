
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'BeamEndReleaseBase',
]


class BeamEndReleaseBase(object):
    """Initialises base Constraint object.

    Parameters
    ----------
    name : str
        Name of the BeamEndRelease object.

    Attributes
    ----------
    name : str
        Name of the BeamEndRelease object.
    """

    def __init__(self):
        self.__name__ = 'ReleaseObject'

    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        l = []
        for attr in self.attr_list:
            l.append('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(l))
