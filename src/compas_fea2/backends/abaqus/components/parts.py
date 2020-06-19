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





    # # ==============================================================================
    # # Helpers
    # # ==============================================================================
    #### TODO ceck!
    # def add_nodes_elements_from_mesh(self, mesh, element_type, thermal=False, elset=None):
    #     """Adds the nodes and faces of a Mesh to the Structure object.

    #     Parameters
    #     ----------
    #     mesh : obj
    #         Mesh datastructure object.
    #     element_type : str
    #         Element type: 'ShellElement', 'MembraneElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     elset : str
    #         Name of element set to create.

    #     Returns
    #     -------
    #     list
    #         Keys of the created elements.
    #     """
    #     ekeys = super(Part, self).add_nodes_elements_from_mesh(mesh, element_type, thermal)
    #     if elset:
    #         self.add_set(name=elset, type='element', selection=ekeys)
    #     return ekeys

    # def add_nodes_elements_from_network(self, network, element_type, thermal=False, axes={}, elset=None):
    #     """Adds the nodes and edges of a Network to the Structure object.

    #     Parameters
    #     ----------
    #     network : obj
    #         Network datastructure object.
    #     element_type : str
    #         Element type: 'BeamElement', 'TrussElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez' for all elements.
    #     elset : str
    #         Name of element set to create.

    #     Returns
    #     -------
    #     list
    #         Keys of the created elements.

    #     """
    #     ekeys = super(Structure, self).add_nodes_elements_from_network(network, element_type, thermal, axes)
    #     if elset:
    #         self.add_set(name=elset, type='element', selection=ekeys)
    #     return ekeys

    # def add_nodes_elements_from_volmesh(self, volmesh, element_type='SolidElement', thermal=False, axes={}, elset=None):
    #     """Adds the nodes and cells of a VolMesh to the Structure object.

    #     Parameters
    #     ----------
    #     volmesh : obj
    #         VolMesh datastructure object.
    #     element_type : str
    #         Element type: 'SolidElement' or ....
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez' for all elements.
    #     elset : str
    #         Name of element set to create.

    #     Returns
    #     -------
    #     list
    #         Keys of the created elements.

    #     """
    #     ekeys = super(Structure, self).add_nodes_elements_from_volmesh(volmesh, element_type, thermal, axes)
    #     if elset:
    #         self.add_set(name=elset, type='element', selection=ekeys)
    #     return ekeys


    # # ==============================================================================
    # # Add Elements
    # # ==============================================================================

    # def add_nodal_element(self, node, type, virtual_node=False):
    #     """Adds a nodal element to the Part Object with the possibility of
    #     adding a coincident virtual node. Virtual nodes are added to a node
    #     set called 'virtual_nodes'.

    #     Parameters
    #     ----------
    #     node : int
    #         Node number the element is connected to.
    #     type : str
    #         Element type: 'SpringElement'.
    #     virtual_node : bool
    #         Create a virtual node or not.

    #     Returns
    #     -------
    #     int
    #         Key of the added element.

    #     Notes
    #     -----
    #     - Elements are numbered sequentially starting from 0.

    #     """
    #     if virtual_node:
    #         xyz = self.node_xyz(node)
    #         key = self.virtual_nodes.setdefault(node, self.node_count())
    #         self.nodes[key] = {'x': xyz[0], 'y': xyz[1], 'z': xyz[2],
    #                            'ex': [1, 0, 0], 'ey': [0, 1, 0], 'ez': [0, 0, 1], 'virtual': True}
    #         if 'virtual_nodes' in self.sets:
    #             self.sets['virtual_nodes']['selection'].append(key)
    #         else:
    #             self.sets['virtual_nodes'] = {'type': 'node', 'selection': [key], 'explode': False}
    #         nodes = [node, key]
    #     else:
    #         nodes = [node]

    #     func_dict = {
    #         'SpringElement': SpringElement,
    #     }

    #     ekey = self.element_count()
    #     element = func_dict[type]()
    #     element.nodes = nodes
    #     element.number = ekey
    #     self.elements[ekey] = element
    #     return ekey

    # def add_virtual_element(self, nodes, type, thermal=False, axes={}):
    #     """Adds a virtual element to structure.elements and to element set 'virtual_elements'.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Nodes the element is connected to.
    #     type : str
    #         Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez'.

    #     Returns
    #     -------
    #     int
    #         Key of the added virtual element.

    #     Notes
    #     -----
    #     - Virtual elements are numbered sequentially starting from 0.

    #     """
    #     ekey = self.check_element_exists(nodes, virtual=True)

    #     if ekey is None:
    #         ekey            = self.element_count()
    #         element         = func_dict[type]()
    #         element.axes    = axes
    #         element.nodes   = nodes
    #         element.number  = ekey
    #         element.thermal = thermal

    #         self.virtual_elements[ekey] = element
    #         self.add_element_to_element_index(ekey, nodes, virtual=True)

    #         if 'virtual_elements' in self.sets:
    #             self.sets['virtual_elements']['selection'].append(ekey)
    #         else:
    #             self.sets['virtual_elements'] = {'type': 'virtual_element', 'selection': [ekey],
    #                                             'index': len(self.sets)}
    #     return ekey





    # # ==============================================================================
    # # Sets
    # # ==============================================================================

    # def add_set(self, name, type, selection):
    #     """Adds a node, element or surface set to structure.sets.

    #     Parameters
    #     ----------
    #     name : str
    #         Name of the Set.
    #     type : str
    #         'node', 'element', 'surface_node', surface_element'.
    #     selection : list, dict
    #         The integer keys of the nodes, elements or the element numbers and sides.

    #     Returns
    #     -------
    #     None

    #     """
    #     if isinstance(selection, int):
    #         selection = [selection]
    #     self.sets[name] = Set(name=name, type=type, selection=selection, index=len(self.sets))





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
        # Write sections
        for section in self.elements_by_section.keys():
            section.write_data(self.elsets_by_section[section], f)

    def write_keyword_end(self, f):
        line = "*End Part\n**"
        f.write(line)



if __name__ == "__main__":

    class MaterialBase(object):
        """Initialises base Material object.

        Parameters
        ----------
        name : str
            Name of the Material object.

        Attributes
        ----------
        name : str
            Name of the Material object.
        """

        def __init__(self, name):
            self.__name__  = 'Material'
            self.name      = name
            self.attr_list = ['name']

        def __str__(self):
            print('\n')
            print('compas_fea {0} object'.format(self.__name__))
            print('-' * (len(self.__name__) + 18))
            for attr in self.attr_list:
                print('{0:<11} : {1}'.format(attr, getattr(self, attr)))
            return ''

        def __repr__(self):
            return '{0}({1})'.format(self.__name__, self.name)


    class ElasticIsotropicBase(MaterialBase):
        """Elastic, isotropic and homogeneous material.

        Parameters
        ----------
        name : str
            Material name.
        E : float
            Young's modulus E [Pa].
        v : float
            Poisson's ratio v [-].
        p : float
            Density [kg/m3].
        tension : bool
            Can take tension.
        compression : bool
            Can take compression.
        """

        def __init__(self, name, E, v, p, tension=True, compression=True):
            MaterialBase.__init__(self, name=name)
            self.__name__    = 'ElasticIsotropic'
            self.name        = name
            self.E           = {'E': E}
            self.v           = {'v': v}
            self.G           = {'G': 0.5 * E / (1 + v)}
            self.p           = p
            self.tension     = tension
            self.compression = compression
            self.attr_list.extend(['E', 'v', 'G', 'p', 'tension', 'compression'])


    class SectionBase(object):
        """Initialises base Section object.

        Parameters
        ----------
        name : str
            Section object name.

        Attributes
        ----------
        name : str
            Section object name.
        geometry : dict
            Geometry of the Section.

        """

        def __init__(self, name, material):

            self.__name__ = 'Section'
            self.name     = name
            self.material = material
            self.geometry = {}

        def __str__(self):
            print('\n')
            print('compas_fea {0} object'.format(self.__name__))
            print('-' * (len(self.__name__) + 18))
            print('name  : {0}'.format(self.name))
            for i, j in self.geometry.items():
                print('{0:<5} : {1}'.format(i, j))
            return ''

        def __repr__(self):
            return '{0}({1})'.format(self.__name__, self.name)

    class BoxSectionBase(SectionBase):
        """Hollow rectangular box cross-section for beam elements.

        Parameters
        ----------
        name : str
            Section name.
        b : float
            Width.
        h : float
            Height.
        tw : float
            Web thickness.
        tf : float
            Flange thickness.

        """

        def __init__(self, name, b, h, tw, tf, material):
            SectionBase.__init__(self, name=name, material=material)

            A   = b * h - (b - 2 * tw) * (h - 2 * tf)
            Ap  = (h - tf) * (b - tw)
            Ixx = (b * h**3) / 12. - ((b - 2 * tw) * (h - 2 * tf)**3) / 12.
            Iyy = (h * b**3) / 12. - ((h - 2 * tf) * (b - 2 * tw)**3) / 12.
            p   = 2 * ((h - tf) / tw + (b - tw) / tf)
            J   = 4 * (Ap**2) / p

            self.__name__ = 'BoxSection'
            self.name     = name
            self.geometry = {'b': b, 'h': h, 'tw': tw, 'tf': tf, 'A': A, 'J': J, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0}

    class ElementBase(object):
        """Initialises base Element object.

        Parameters
        ----------
        nodes : list
            Node keys the element connects to.
        number : int
            Number of the element.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes.

        Attributes
        ----------
        nodes : list
            Node keys the element connects to.
        number : int
            Number of the element.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes.
        element_property : str
            Element property name
        """

        def __init__(self, key, eltype, nodes_keys, section, elset=None, thermal=None, axes={}):
            self.__name__         = 'Element'
            self.key              = key
            self.eltype           = eltype
            self.nodes_keys       = nodes_keys
            self.section          = section
            self.thermal          = thermal
            self.axes             = axes
            if not elset:
                self.elset        = self.section.name
            else:
                self.elset        = elset

        def __str__(self):
            print('\n')
            print('compas_fea {0} object'.format(self.__name__))
            print('-' * (len(self.__name__) + 18))
            for attr in ['key', 'nodes_keys', 'thermal', 'axes', 'element_property']:
                print('{0:<10} : {1}'.format(attr, getattr(self, attr)))
            return ''

        def __repr__(self):
            return '{0}({1})'.format(self.__name__, self.key)

    material_one = MaterialBase(name='material_one')
    material_elastic = ElasticIsotropicBase(name='elastic',E=1,v=2,p=3)
    section_A = SectionBase(name='section_A', material=material_one)
    section_B = BoxSectionBase(name='section_B', material=material_elastic, b=10, h=20, tw=2, tf=5)
    el_one = ElementBase(key=1,nodes_keys=[2,3],eltype='beam', section=section_A, elset='group_2')
    el_two = ElementBase(key=2,nodes_keys=[2,3],eltype='solid', section=section_A)
    el_three = ElementBase(key=3,nodes_keys=[2,3],eltype='beam', section=section_B,elset='group_2')
    my_part = Part(name='test', nodes='nodes', elements=[el_one, el_two, el_three])



    # print(my_part.elsets_by_section)
    # for section in my_part.elements_by_section.keys():
    #     print(section.material.name)


        # Write elements
    for eltype in my_part.elements_by_type.keys():
        for elset in my_part.elements_by_elset.keys():
            elements = my_part.elements_by_elset[elset].intersection(my_part.elements_by_type[eltype])
            if elements:
                elements =list(elements)
                elements[0].write_keyword(elset, f)
                for element in elements:
                    element.write_data(f)


    # f=open('C:/temp/test_input.inp','w')
    # my_part.write_data(f)
    # f.close()

    # # print(type(my_part.elements_by_section[section_A]))

