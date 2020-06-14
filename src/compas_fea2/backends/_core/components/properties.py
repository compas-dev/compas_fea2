from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez),
#            Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'ElementPropertiesBase'
]


class ElementPropertiesBase(object):
    """Initialises an ElementProperties object.

    Parameters
    ----------
    name : str
        Key name for the ElementProperties object.
    material : str
        Name of the Material object to assign.
    section : str
        Name of the Section object to assign.
    elements : list
        Element keys assignment.

    Attributes
    ----------
    name : str
        Key name for the ElementProperties object.
    material : str
        Name of the Material object to assign.
    section : str
        Name of the Section object to assign.
    elements : list
        Element keys assignment.
    """

    def __init__(self, name, material=None, section=None, elements=None, rebar=None):
        self.__name__ = 'ElementProperties'
        self.name     = name
        self.material = material
        self.section  = section
        self.elements = elements
        self.rebar    = rebar
        # if (not elset) and (not elements):
        #     raise NameError('***** ElementProperties objects require elements or element sets *****') #TODO move to abaqus only

    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))
        for attr in ['name', 'material', 'section', 'collection', 'elements']:
            print('{0:<13} : {1}'.format(attr, getattr(self, attr)))
        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)
