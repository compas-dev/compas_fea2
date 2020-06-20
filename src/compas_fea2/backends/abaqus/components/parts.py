from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class Part():
    """Initialises the Part object.

    """
    def __init__(self, name, nodes, elements, nsets=None, elsets=None):
        self.__name__ = 'Part'
        self.name = name
        self.nodes = nodes  # list with the Node Objects
        self.elements = elements  # list of Element Objects
        self.nsets = nsets
        self.elsets = elsets

        groups = self._group_elements()
        self.elements_by_type = groups[0]
        self.elements_by_section = groups[1]
        self.elements_by_elset = groups[2]
        self.elsets_by_section = groups[3]

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _group_elements(self):  #TODO this can be done better...
        el_dict={}
        for el in self.elements:
            el_dict[el] = (el.eltype, el.section, el.elset)
        type_elements = {}
        section_elements = {}
        elset_elements = {}
        section_elsets = {}
        for key, value in el_dict.items():
            type_elements.setdefault(value[0], set()).add(key)
            section_elements.setdefault(value[1], set()).add(key)
            elset_elements.setdefault(value[2], set()).add(key)
            section_elsets.setdefault(value[1], set()).add(value[2])

        return type_elements, section_elements, elset_elements, section_elsets


    # ==============================================================================
    # Write to input file
    # ==============================================================================

    def write_keyword_start(self, f):
        line = "*Part, name={}".format(self.name)
        f.write(line)

    def write_data(self, f):
        # Write nodes
        self.nodes[0].write_keyword(f)
        for node in self.nodes:
            node.write_data(f)
        # Write elements
        for eltype in self.elements_by_type.keys():
            for elset in self.elements_by_elset.keys():
                elements = self.elements_by_elset[elset].intersection(self.elements_by_type[eltype])
                if elements:
                    elements = list(elements)
                    elements[0].write_keyword(f)
                    for element in elements:
                        element.write_data(f)
        # Write node sets
        for nset in self.nsets:
            nset.write_keyword(f)
            nset.write_data(f)
        # Write elements sets
        for elset in self.elsets:
            elset.write_keyword(f)
            elset.write_data(f)
        # Write sections ()
        for section in self.elements_by_section.keys():
            for elset in elsets_by_section[section]:
                section.write_data(elset, f)

    def write_keyword_end(self, f):
        line = "*End Part\n**"
        f.write(line)



if __name__ == "__main__":

    from compas_fea2.backends.abaqus.components import Node
    from compas_fea2.backends.abaqus.components import Concrete
    from compas_fea2.backends.abaqus.components import ElasticIsotropic
    from compas_fea2.backends.abaqus.components import BoxSection
    from compas_fea2.backends.abaqus.components import SolidSection
    from compas_fea2.backends.abaqus.components import BeamElement
    from compas_fea2.backends.abaqus.components import SolidElement

    my_nodes = []
    for k in range(5):
        my_nodes.append(Node(k,[1,2,3]))
    material_one = Concrete('my_mat',1,2,3,4)
    material_elastic = ElasticIsotropic(name='elastic',E=1,v=2,p=3)
    section_A = SolidSection(name='section_A', material=material_one)
    section_B = BoxSection(name='section_B', material=material_elastic, b=10, h=20, tw=2, tf=5)
    el_one = SolidElement(key=1, connectivity=[2,3,4,5], section=section_A, elset='group_2')
    el_two = SolidElement(key=2, connectivity=[2,3,4,5], section=section_A)
    el_three = BeamElement(key=3, connectivity=[2,3], section=section_B, elset='group_2')
    my_part = Part(name='test', nodes=my_nodes, elements=[el_one, el_two, el_three])


    f=open('C:/temp/test_input.inp','w')
    my_part.write_data(f)
    f.close()

    # # print(type(my_part.elements_by_section[section_A]))

