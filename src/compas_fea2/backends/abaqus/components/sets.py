
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

    #TODO generate option might not be a good idea!
    def __init__(self, name, selection, generate=False, instance=None):

        self.__name__  = 'Set'
        self.name      = name
        self.selection = selection
        self.generate  = generate
        if self.selection[0].__name__ == 'Node':
            self.stype = 'nset'
        else:
            self.stype = 'elset'
        self.instance = instance

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



# class PartNSet(Set):
#     def __init__(self, name, selection):
#         super(Set, self).__init__(name)
#         self.part = part
#         self.stype = 'nset'
#         self.domain = 'part'
#         self.data = self._generate_data()


# class PartElSet(Set):
#     def __init__(self, name, selection):
#         super(Set, self).__init__(name, selection)
#         self.part = None
#         self.type = 'elset'
#         self.domain = 'part'
#         self.data = self._generate_data()


# class AssemblyNSet(Set):
#     def __init__(self, name, selection, instance):
#         super(Set, self).__init__(name)
#         self.instance = instance
#         self.type = 'nset'
#         self.domain = 'assembly'
#         self.data = self._generate_data()


# class AssemblyElSet(Set):
#     def __init__(self, name, selection, instance):
#         super(Set, self).__init__(name, selection)
#         self.instance = instance
#         self.type = 'elset'
#         self.domain = 'assembly'
#         self.data = self._generate_data()
