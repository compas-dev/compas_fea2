
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Set',
]


class Set(object):

    """ Initialises base Set object.

    Parameters
    ----------
    name : str
        Name of the set.
    type : str
        'node', 'element', 'surface_node', surface_element'.
    selection : list, dict
        The integer keys of the nodes, elements or the element numbers and sides.
    index : int
        Set index number.

    Attributes
    ----------
    name : str
        Name of the set.
    type : str
        'node', 'element', 'surface_node', surface_element'.
    selection : list, dict
        The integer keys of the nodes, elements or the element numbers and sides.
    index : int
        Set index number.

    """

    def __init__(self, name, selection, generate=False):

        self.__name__  = 'Set'
        self.name      = name
        self.selection = selection
        self.generate  = generate

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name', 'type', 'selection', 'index']:
            print('{0:<9} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)

    def write_data(self, f):
        if self.generate:
            line    = '{0}, {1}, 1'.format(self.selection[0].key, self.selection[-1].key)
            f.write(line)
        else:
            for s in self.selection:  # note: can be grouped in 16 elements
                line    = ''.format(s.key)
                f.write(line)



class PartNSet(Set):
    def __init__(self, name, selection, part):
        super(Set, self).__init__(name)
        self.part = part
        self.type = 'nset'
        self.domain = 'part'

    def write_keyword(self, f):
        if self.generate:
            g =", generate"
        else:
            g=""
        line = "*Nset, nset={}{}".format(self.name, g)
        f.write(line)

class PartElSet(Set):
    def __init__(self, name, selection, sections, part):
        super(Set, self).__init__(name, selection)
        self.part = part
        self.type = 'elset'
        self.domain = 'part'

    def write_keyword(self, f):
        if self.generate:
            g =", generate"
        else:
            g=""
        line = "*Elset, elset={}{}".format(self.name, g)
        f.write(line)


class AssemblyNSet(Set):
    def __init__(self, name, selection, instance, assembly):
        super(Set, self).__init__(name)
        self.assembly = assembly
        self.instance = instance
        self.type = 'nset'
        self.domain = 'assembly'

    def write_keyword(self, f):
        if self.generate:
            g =", generate"
        else:
            g=""
        line = "*Nset, nset={}, instance={}{}".format(self.name, self.instance, g)
        f.write(line)

class AssemblyElSet(Set):
    def __init__(self, name, selection, instance, assembly):
        super(Set, self).__init__(name, selection)
        self.assembly = assembly
        self.instance = instance
        self.type = 'elset'
        self.domain = 'assembly'

    def write_keyword(self, f):
        if self.generate:
            g =", generate"
        else:
            g=""
        line = "*Elset, elset={}, instance={}{}".format(self.name, self.instance, g)
        f.write(line)
