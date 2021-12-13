
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase

# Author(s): Francesco Ranaudo (github.com/franaudo)


class GroupBase(FEABase):

    """Initialises a base Set object.

    Parameters
    ----------
    name : str
        Name of the group.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    """

    def __init__(self, name, selection):

        self.__name__ = 'Set'
        self._name = name
        self._selection = selection
        self._instance = None

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def selection(self):
        """The selection property."""
        return self._selection

    @property
    def instance(self):
        """The instance property."""
        return self._instance

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class NodesGroupBase(GroupBase):
    def __init__(self, name, selection):
        super(NodesGroupBase, self).__init__(name, selection)


class ElementsGroupBase(GroupBase):
    def __init__(self, name, selection):
        super(ElementsGroupBase, self).__init__(name, selection)


class SurfaceBase(FEABase):
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

    # TODO check http://130.149.89.49:2080/v6.14/books/usb/default.htm?startat=pt01ch02s03aus17.html#usb-int-adeformablesurf
    def __init__(self, name, set, generate=False):

        self.__name__ = 'Set'
        self.name = name
        self.selection = selection
        self.generate = generate
        if self.selection[0].__name__ == 'Node':
            self.stype = 'nset'
        else:
            self.stype = 'elset'
        self.instance = None
