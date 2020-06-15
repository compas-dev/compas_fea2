from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class Assembly():
    """Initialises the Part object.

    """

    def __init__(self, name, instance=None, nsets=None, elsets=None, surfaces=None, features=None, engineering_features=None):
        self.__name__ = 'Assembly'
        self.name = name
        self.nsets = nsets
        self.elsets = elsets
        self.surfaces = surfaces
        self.features = features
        self.engineering_features = engineering_features

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


if __name__ == "__main__":

    my_assembly = Assembly(name='test')

    print(my_assembly)
