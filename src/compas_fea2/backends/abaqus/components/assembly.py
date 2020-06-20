from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = [
    'Assembly',
    'Instance',
]

class Assembly():
    """Initialises the Assembly object.

    """

    def __init__(self, name, instances=None, nsets=None, elsets=None, surfaces=None):
        self.__name__ = 'Assembly'
        self.name       = name
        self.instances  = instances
        self.nsets      = nsets
        self.elsets     = elsets
        self.surfaces   = surfaces

        self.parts_by_material = self._get_materials()

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)

    def _get_materials(self):
        materials = []
        for i in self.instances:
            for mat in i.part.elements_by_material.keys():
                materials.append(mat)
        return list(set(materials))

    def write_keyword_start(self, f):
        line = """
**
** ASSEMBLY
**
*Assembly, name={}
**\n""".format(self.name)

        f.write(line)

    def write_keyword_end(self, f):
        line = """*End Assembly
**
** MATERIALS
**\n"""
        f.write(line)

class Instance():
    """Initialises the Instance object.

    """

    def __init__(self, name, part):
        self.__name__ = 'Instance'
        self.name = name
        self.part = part

    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    def write_data(self, f):
        line = """*Instance, name={}, part={}
*End Instance
**\n""".format(self.name, self.part.name)
        f.write(line)



if __name__ == "__main__":
    from compas_fea2.backends.abaqus.components import Node
    from compas_fea2.backends.abaqus.components import Concrete
    from compas_fea2.backends.abaqus.components import ElasticIsotropic
    from compas_fea2.backends.abaqus.components import BoxSection
    from compas_fea2.backends.abaqus.components import SolidSection
    from compas_fea2.backends.abaqus.components import BeamElement
    from compas_fea2.backends.abaqus.components import SolidElement
    from compas_fea2.backends.abaqus.components import Part

    my_nodes = []
    for k in range(5):
        my_nodes.append(Node(k,[1+k,2-k,3]))

    material_one = Concrete('my_mat',1,2,3,4)
    material_elastic = ElasticIsotropic(name='elastic',E=1,v=2,p=3)

    section_A = SolidSection(name='section_A', material=material_one)
    section_B = BoxSection(name='section_B', material=material_elastic, b=10, h=20, tw=2, tf=5)

    el_one = SolidElement(key=0, connectivity=my_nodes[:4], section=section_A)
    el_two = SolidElement(key=1, connectivity=my_nodes[:4], section=section_A)
    el_three = SolidElement(key=2, connectivity=my_nodes[1:5], section=section_A)
    el_4 = SolidElement(key=3, connectivity=my_nodes[:4], section=section_A)

    my_part = Part(name='test', nodes=my_nodes, elements=[el_one, el_two, el_three, el_4])
    my_instance = Instance(name='test_instance', part=my_part)
    my_assembly = Assembly(name='test', instances=[my_instance])

    print(my_assembly.parts_by_material)
    # f=open('/home/fr/Downloads/test_input.inp','w')
    f=open('C:/temp/test_input.inp','w')
    my_part.write_keyword_start(f)
    my_part.write_data(f)
    my_part.write_keyword_end(f)
    my_assembly.write_keyword_start(f)
    # Write instances
    for instance in my_assembly.instances:
        instance.write_data(f)
    my_assembly.write_keyword_end(f)
    f.close()

    # # print(type(my_part.elements_by_section[section_A]))
