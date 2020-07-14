from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

import sys

__all__ = [
    'Model',
    'Instance',
]

class Model():
    """Initialises Model object. This is in many aspects equivalent to an
    `Assembly` in Abaqus.

    Parameters
    ----------
    name : str
        Name of the Assembly.

    Attributes
    ----------
    name : str
        Name of the Assembly.
    parts : list
        A list with the Part objects referenced in the Assembly.
    instances : list
        A list with the Instance objects belonging to the Assembly.
    parts : list
        A list with the Part objects referenced in the Assembly.
    surfaces : list
        A list with the Surface objects belonging to the Assembly.
    constraints : list
        A list with the Constraint objects belonging to the Assembly.
    materials : list
        A list of all the materials defined int the Assembly.

    """

    def __init__(self, name, ):
        self.__name__       = 'Model'
        self.name           = name
        self.instances      = {}
        self.parts          = {}
        self.surfaces       = []
        self.constraints    = []
        self.add_interactions = []
        self.materials      = {}
        self.sections       = {}
        self.sets           = {}
        # self.materials      = self._get_materials()

        # self.data           = self._generate_data()

    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        data = []
        for attr in ['name']:
            data.append('{0:<15} : {1}'.format(attr, getattr(self, attr)))

        data.append('{0:<15} : {1}'.format('# of parts', len(self.parts)))
        data.append('{0:<15} : {1}'.format('# of instances', len(self.instances)))
        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(data))


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)

    def _get_materials(self):
        materials = []
        for i in self.instances:
            for mat in i.part.elements_by_material.keys():
                materials.append(mat)
        return list(set(materials))

    def _generate_data(self):
        line = '*Assembly, name={}\n**\n'.format(self.name)
        section_data = [line]
        for instance in self.instances.values():
            section_data.append(instance._generate_data())
            for iset in instance.sets:
                section_data.append(iset._generate_data())
        # for surface in self.surfaces:
        #     section_data.append(surface.data)
        # for constraint in self.constraints:
        #     section_data.append(constraint.data)
        line = '*End Assembly\n**'
        section_data.append(line)
        return ''.join(section_data)

    # =========================================================================
    #                            General methods
    # =========================================================================


    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def add_part(self, part, transformation={}):
        """Adds a Part to the Assembly and creates an Instance object from the
        specified Part and adds it to the Assembly. If a transformation matrix
        is specified, the instance is creteated in the transformed location.

        Parameters
        ----------
        part : obj
            Part object from which the Instance is created.
        transformation : dict
            Dictionary containing the trasformation matrices to apply to the Part
            before creating the Instances.
            key: (str) instance name
            value: (matrix) transformation matrix

        Returns
        -------
        None

        Examples
        --------
        In this example a part is added to the model and two instances are created
        using two transformation matrices.
        >>> model = Assembly('mymodel')
        >>> part = Part('mypart')
        >>> model.add_part(part=part, transformation=[M1, M2])
        """

        if part.name in self.parts.keys():
            print("WARNING: Part {} already in the Assembly. Part not added!".format(part.name))
        else:
            self.parts[part.name] = part

        if transformation:
            for i in transformation.keys():
                instance = self._instance_from_part(part, i, transformation[i])
                self.add_instance(instance)
        else:
            self.add_instance(Instance('{}-{}'.format(part.name, 1), part))

    def remove_part(self, part):
        """ Removes the part from the assembly and all the referenced instances
        of that part.

        Parameters
        ----------
        part : str
            Name of the Part to remove.

        Returns
        -------
        None
        """

        self.parts.pop(part)

        for instance in self.instances:
            if self.instances[instance].part.name == part:
                self.instances.pop(instance)

    # =========================================================================
    #                          Instances methods
    # =========================================================================
    def add_instance(self, instance):
        """Adds a compas_fea2 Instance object to the Assembly. If the Part to
        which the instance is referred to does not exist, it is automatically
        created.

        Parameters
        ----------
        instance : obj
            compas_fea2 Instance object.

        Returns
        -------
        None
        """
        if instance.name not in self.instances.keys():
            self.instances[instance.name]= instance
            if instance.part.name not in self.parts.keys():
                self.parts[part.name] = instance.part
        else:
            print('Duplicate instance {} will be ignored!'.format(instance.name))

    def remove_instance(self, instance):
        """ Removes the part from the assembly and all the referenced instances.

        Parameters
        ----------
        instace : str
            Name of the Instance object to remove.

        Returns
        -------
        None
        """

        self.instances.pop(instance)

    def _instance_from_part(self, part, instance_name, transformation):
        pass

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def add_node(self, node, part):
        """Adds a compas_fea2 Node object to a Part in the Assmbly.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are autmatically excluded.
        The part must have been previously added to the Assembly.

        Parameters
        ----------
        node : obj
            compas_fea2 Node object.
        part : str
            Name of the part where the node will be added.

        Returns
        -------
        None
        """
        error_code=0
        if part in self.parts.keys():
            self.parts[part].add_node(node)
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the assembly!'.format(part))

    def add_nodes(self, nodes, part):
        """Add multiple compas_fea2 Node objects a Part in the Assmbly.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are autmatically excluded.
        The part must have been previously added to the Assembly.

        Parameters
        ----------
        nodes : list
            List of compas_fea2 Node objects.
        part : str
            Name of the part where the node will be added.

        Returns
        -------
        None
        """

        for node in nodes:
            self.add_node(node, part)

    def remove_node(self, node_key, part):
        '''Remove the node from a Part in the Assmbly. If there are duplicate nodes,
        it removes also all the duplicates.

        Parameters
        ----------
        node_key : int
            Key number of the node to be removed.
        part : str
            Name of the part where the node will be removed from.

        Returns
        -------
        None
        '''
        error_code=0
        if part in self.parts.keys():
            self.parts[part].remove_node(node_key)
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the assembly!'.format(part))

    def remove_nodes(self, nodes, part):
        '''Remove the nodes from a Part in the Assmbly. If there are duplicate nodes,
        it removes also all the duplicates.

        Parameters
        ----------
        node : list
            List with the key numbers of the nodes to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        for node in nodes:
            self.remove_node(node, part)

    # =========================================================================
    #                           Elements methods
    # =========================================================================
    def add_element(self, element, part):
        """Adds a compas_fea2 Element object to a Part in the Assmbly.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        error_code=0
        if part in self.parts.keys():
            self.parts[part].add_element(element)
            if element.section not in self.sections.keys():
                sys.exit('ERROR: section {} not found in the assembly!'.format(element.section))
            elif element.section not in self.parts[part].sections.keys():
                self.parts[part].sections[element.section] = self.sections[element.section]
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the assembly!'.format(part))

    def add_elements(self, elements, part):
        """Adds multiple compas_fea2 Element objects to a Part in the Assmbly.

        Parameters
        ----------
        elements : list
            List of compas_fea2 Element objects.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        for element in elements:
            self.add_element(element, part)

    def remove_element(self, element_key, part):
        '''Removes the element from a Part in the Assmbly.

        Parameters
        ----------
        element_key : int
            Key number of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''
        error_code=0
        if part in self.parts.keys():
            self.parts[part].remove_element(element_key)
            error_code=1

        if error_code == 0:
            sys.exit('ERROR: part {} not found in the assembly!'.format(part))

    def remove_elements(self, elements, part):
        '''Removes the elements from a Part in the Assmbly.

        Parameters
        ----------
        elements : list
            List with the key numbers of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        for element in elements:
            self.remove_node(element, part)

    # =========================================================================
    #                               Sets methods
    # =========================================================================
    def add_part_node_set(self, part, nset):
        pass

    def add_assembly_set(self, set, instance):
        '''Adds a Set object to the Assembly.

        Parameters
        ----------
        set : obj
            node set object.
        instance : str
            Name of the instance where the set belongs to.

        Returns
        -------
        None
        '''
        if instance not in self.instances.keys():
            sys.exit('ERROR: instance {} not found in the assembly!'.format(instance))
        set.instance = instance
        self.instances[instance].sets.append(set)

        self.sets[set.name] = set

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        '''Adds a Material object to the Assembly so that it can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            compas_fea2 material object.

        Returns
        -------
        None
        '''
        if material.name not in self.materials.keys():
            self.materials[material.name] = material

    def add_materials(self, materials):
        '''Adds multiple Material objects to the Assembly so that they can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : list
            List of compas_fea2 material objects.

        Returns
        -------
        None
        '''
        for material in materials:
            self.add_material(material)

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def add_section(self, section):
        """Adds a compas_fea2 Section object to the Assmbly.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        if section.name not in self.sections.keys():
            self.sections[section.name] = section
            if section.material not in self.materials.keys():
                sys.exit('ERROR: material {} not found in the assembly!'.format(section.material))
            self.add_material(self.materials[section.material])






    # =========================================================================
    #                        Surfaces methods
    # =========================================================================
    def add_surface(self, surface):
        self.surfaces.append(surface)


    # =========================================================================
    #                       Constraints methods
    # =========================================================================
    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    # def add_instance_set(self, iset, instance):
    #     """ Adds a set to a previously defined Instance.

    #     Parameters
    #     ----------
    #     part : obj
    #         Part object from which the Instance is created.
    #     transformation : matrix
    #         Trasformation matrix to apply to the Part before creating the Instance.
    #     """
    #     self.instances[instance].sets.append(iset)

    # =========================================================================
    #                        Interaction methods
    # =========================================================================

    def add_interactions(self, interactions):
        pass


class Instance():
    """Initialises base Instance object.

    Parameters
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
    sets : list
        A list with the Set objects belonging to the instance.

    Attributes
    ----------
    name : str
        Name of the set.
    part : Part object
        The part from which create the instance.
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

        self.data = """*Instance, name={}, part={}\n*End Instance\n**\n""".format(self.name, self.part.name)

    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.part.name)

    def _generate_data(self):
        return """*Instance, name={}, part={}\n*End Instance\n**\n""".format(self.name, self.part.name)

if __name__ == "__main__":
    from compas_fea2.backends.abaqus.components import Node
    from compas_fea2.backends.abaqus.components import Concrete
    from compas_fea2.backends.abaqus.components import ElasticIsotropic
    from compas_fea2.backends.abaqus.components import BoxSection
    from compas_fea2.backends.abaqus.components import SolidSection
    from compas_fea2.backends.abaqus.components import BeamElement
    from compas_fea2.backends.abaqus.components import SolidElement
    from compas_fea2.backends.abaqus.components import Part
    from compas_fea2.backends.abaqus.components import Set

    my_nodes = []
    for k in range(5):
        my_nodes.append(Node(k,[1+k,2-k,3]))

    material_one = ElasticIsotropic(name='elastic',E=1,v=2,p=3)
    material_elastic = ElasticIsotropic(name='elastic',E=1,v=2,p=3)

    section_A = SolidSection(name='section_A', material=material_one)
    section_B = BoxSection(name='section_B', material=material_elastic, b=10, h=20, tw=2, tf=5)

    el_one = SolidElement(key=0, connectivity=my_nodes[:4], section=section_A)
    el_two = SolidElement(key=1, connectivity=my_nodes[:4], section=section_A)
    el_three = SolidElement(key=2, connectivity=my_nodes[1:5], section=section_A)
    el_4 = SolidElement(key=3, connectivity=my_nodes[:4], section=section_A)

    my_part = Part(name='test', nodes=my_nodes, elements=[el_one, el_two, el_three, el_4])

    nset = Set('test_neset', my_nodes)

    my_instance = Instance(name='test_instance', part=my_part, sets=[nset])
    my_assembly = Assembly(name='test', instances=[my_instance])

    print(my_assembly.data)
