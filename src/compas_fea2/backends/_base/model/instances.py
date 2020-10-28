from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [
    'InstanceBase',
]


class InstanceBase():
    """Initialises a base Instance object.

    Parameters
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
    sets : list
        A list with the Set objects belonging to the instance.
    data : str
        The data block for the generation of the input file.
    """

    def __init__(self, name, part, sets=[]):
        self.__name__ = 'Instance'
        self.name = name
        self.part = part
        self.sets = sets
        for iset in sets:
            iset.instance = self.name
            iset.data = iset._generate_data()

        self.data = """*Instance, name={}, part={}\n*End Instance\n**\n""".format(
            self.name, self.part.name)

    def __str__(self):
        print('\n')
        print('compas_fea2 {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.part.name)



# =============================================================================
#                               Debugging
# =============================================================================

if __name__ == "__main__":
    pass
