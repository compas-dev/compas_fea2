
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Set',
]


class Set(object):

    """Initialises base Set object.

    Parameters
    ----------
    name : str
        Name of the set.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    #TODO generate option might not be a good idea!
    def __init__(self, name, selection, generate=False):

        self.__name__  = 'Set'
        self.name      = name
        self.selection = selection
        self.generate  = generate
        if self.selection[0].__name__ == 'Node':
            self.stype = 'nset'
        else:
            self.stype = 'elset'
        self.instance = None

        self.data = self._generate_data()

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name', 'type', 'selection', 'index']:
            print('{0:<9} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)

    def _generate_data(self):
        data_section = []
        line = '*{}, {}={}'.format(self.stype, self.stype, self.name)
        if self.instance:
            line = ', instance='.join([line, self.instance])
        if self.generate:
            line = ', '.join([line, 'generate'])
            data_section.append(line)
            data_section.append('{0}, {1}, 1'.format(self.selection[0].key, self.selection[-1].key))
        else:
            data_section.append(line)
            for s in self.selection:
                # note: can be grouped in 16 elements
                data_section.append(str(s.key))
        return '\n'.join(data_section) + '\n'
