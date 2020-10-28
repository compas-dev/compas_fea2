
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'SetBase',
    'SurfaceBase',
]


class SetBase(object):

    """Initialises a base Set object.

    Parameters
    ----------
    name : str
        Name of the set.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    stype : str
        Node or Element set identifier. It can be either 'nset' or 'elset'
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    #TODO generate option might not be a good idea!
    def __init__(self, name, selection, stype, generate=False):

        self.__name__  = 'Set'
        self.name      = name
        self.selection = selection
        self.generate  = generate
        self.stype = stype
        # if self.selection[0].__name__ == 'Node':
        #     self.stype = 'nset'
        # else:
        #     self.stype = 'elset'
        self.instance = None


    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        data = []
        for attr in ['name', 'type', 'selection', 'index']:
            data.append('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(data))

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


class SurfaceBase():
    """Initialises the Surfaces object.

    Parameters
    ----------
    name : str
        Name of the set.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    #TODO check http://130.149.89.49:2080/v6.14/books/usb/default.htm?startat=pt01ch02s03aus17.html#usb-int-adeformablesurf
    def __init__(self, name, set, generate=False):

        self.__name__  = 'Set'
        self.name      = name
        self.selection = selection
        self.generate  = generate
        if self.selection[0].__name__ == 'Node':
            self.stype = 'nset'
        else:
            self.stype = 'elset'
        self.instance = None

