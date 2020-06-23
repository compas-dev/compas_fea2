
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

# from compas_fea2.backends._core import ElementPropertiesBase

# # Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


# __all__ = [
#     'ElementProperties'
# ]


# class ElementProperties(ElementPropertiesBase):

#     """ Initialises an ElementProperties object.

#     Parameters
#     ----------
#     name : str
#         Key name for the ElementProperties object.
#     material : str
#         Name of the Material object to assign.
#     section : str
#         Name of the Section object to assign.
#     elset : str
#         Element set name.
#     elements : list
#         Element keys assignment.
#     rebar : dict
#         Reinforcement layer data.

#     Attributes
#     ----------
#     name : str
#         Key name for the ElementProperties object.
#     material : str
#         Name of the Material object to assign.
#     section : str
#         Name of the Section object to assign.
#     elset : str
#         Element set name.
#     elements : list
#         Element keys assignment.
#     rebar : dict
#         Reinforcement layer data.

#     Notes
#     -----
#     - Either ``elements`` or ``elset`` should be given, not both.

#     """

#     def __init__(self, name, material=None, section=None, elset=None, elements=None, rebar=None, collection=None):
#         super(ElementProperties, self).__init__(name, material, section, elements, collection)
#         self.elset    = elset
#         self.rebar    = rebar

#         if (not elset) and (not elements):
#             raise NameError('***** ElementProperties objects require elements or element sets *****')


#     def __str__(self):

#         print('\n')
#         print('compas_fea {0} object'.format(self.__name__))
#         print('-' * (len(self.__name__) + 18))

#         for attr in ['name', 'material', 'section', 'elset', 'elements', 'rebar']:
#             print('{0:<13} : {1}'.format(attr, getattr(self, attr)))

#         return ''
