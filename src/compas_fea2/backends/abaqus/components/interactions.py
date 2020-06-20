from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = [
    'Interaction',
]

class Interaction():
    """Initialises the Interaction object.

    """
    pass
    # def __init__(self, name, nodes, elements, nsets=[], elsets=[]):
    #     self.__name__ = 'Part'
    #     self.name = name
    #     self.nodes = self._sort(nodes)
    #     self.elements = self._sort(elements)
    #     self.nsets = nsets
    #     self.elsets = elsets

    #     groups = self._group_elements()
    #     self.elements_by_type = groups[0]
    #     self.elements_by_section = groups[1]
    #     self.elements_by_elset = groups[2]
    #     self.elsets_by_section = groups[3]
    #     self.elements_by_material = groups[4]

    # def __str__(self):

    #     print('\n')
    #     print('compas_fea {0} object'.format(self.__name__))
    #     print('-' * (len(self.__name__) + 18))

    #     for attr in ['name']:
    #         print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

    #     return ''

    # def __repr__(self):

    #     return '{0}({1})'.format(self.__name__, self.name)


    # # ==============================================================================
    # # Constructor methods
    # # ==============================================================================
    # def _sort(self, attr):
    #     return sorted(attr, key=lambda x: x.key, reverse=False)

    # def _group_elements(self):  #TODO this can be done better...
    #     el_dict={}
    #     for el in self.elements:
    #         el_dict[el] = (el.eltype, el.section, el.elset)
    #     type_elements = {}
    #     section_elements = {}
    #     elset_elements = {}
    #     section_elsets = {}
    #     material_elements = {}
    #     for key, value in el_dict.items():
    #         type_elements.setdefault(value[0], set()).add(key)
    #         section_elements.setdefault(value[1], set()).add(key)
    #         material_elements.setdefault(value[1].material, set()).add(key)
    #         elset_elements.setdefault(value[2], set()).add(key)
    #         section_elsets.setdefault(value[1], set()).add(value[2])


    #     # section_elements = sorted(section_elements, key=lambda x: x.key, reverse=True)

    #     return type_elements, section_elements, elset_elements, section_elsets, material_elements


    # # ==============================================================================
    # # Write to input file
    # # ==============================================================================

    # def write_keyword_start(self, f):
    #     line = "*Part, name={}\n".format(self.name)
    #     f.write(line)

    # def write_data(self, f):
    #     # Write nodes
    #     self.nodes[0].write_keyword(f)
    #     for node in self.nodes:
    #         node.write_data(f)
    #     # Write elements
    #     for eltype in self.elements_by_type.keys():
    #         for elset in self.elements_by_elset.keys():
    #             elements = self.elements_by_elset[elset].intersection(self.elements_by_type[eltype])
    #             elements = sorted(elements, key=lambda x: x.key, reverse=False)
    #             if elements:
    #                 elements = list(elements)
    #                 elements[0].write_keyword(f)
    #                 for element in elements:
    #                     element.write_data(f)
    #     # Write node sets
    #     for nset in self.nsets:
    #         nset.write_keyword(f)
    #         nset.write_data(f)
    #     # Write elements sets
    #     for elset in self.elsets:
    #         elset.write_keyword(f)
    #         elset.write_data(f)
    #     # Write sections ()
    #     for section in self.elements_by_section.keys():
    #         for elset in self.elsets_by_section[section]:
    #             section.write_data(elset, f)

    # def write_keyword_end(self, f):
    #     line = "*End Part\n**"
    #     f.write(line)
