from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

import pickle
import os
import importlib

__all__ = [
    'ModelBase',
]


class ModelBase():
    """Initialises a base Model object.

    Parameters
    ----------
    name : str
        Name of the Model.

    Attributes
    ----------
    name : str
        Name of the Model.
    parts : list
        A list with the `Part` objects referenced in the Model.
    instances : dict
        A dictionary with the `Instance` objects belonging to the Model.
    surfaces : list
        A list with the `Surface` objects belonging to the Model.
    constraints : list
        A list with the `Constrain`t objects belonging to the Model.
    interactions : list
        A list with the `Interaction` objects belonging to the Model.
    materials : dict
        A dictionary of all the materials defined in the Model.
    sections : dict
        A dictionary of all the sections defined in the Model.
    sets : dict
        A dictionary of all the sets defined in the Model.
    """

    def __init__(self, name):
        self.__name__ = 'Model'
        self.name = name
        self.instances = {}
        self.parts = {}
        self.surfaces = []
        self.constraints = []
        self.interactions = []
        self.materials = {}
        self.sections = {}
        self.sets = {}
        # self.materials      = self._get_materials()
        # self.data           = self._generate_data()

    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        data = []
        for attr in ['name']:
            data.append('{0:<15} : {1}'.format(attr, getattr(self, attr)))

        data.append('{0:<15} : {1}'.format('# of parts', len(self.parts)))
        data.append('{0:<15} : {1}'.format(
            '# of instances', len(self.instances)))
        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(data))

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    def _get_materials(self):
        materials = []
        for i in self.instances:
            for mat in i.part.elements_by_material.keys():
                materials.append(mat)
        return list(set(materials))

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    def from_network(self, network):
        raise NotImplementedError()

    def from_obj(self, obj):
        raise NotImplementedError()

    def frame_from_mesh(self, mesh, beam_section):
        """Creates a Model object from a compas Mesh object [WIP]. The edges of
        the mesh become the elements of the frame. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        mesh : obj
            Mesh to convert to import as a Model.
        beam_section : obj
            compas_fea2 BeamSection object to to apply to the frame elements.
        """
        from compas.geometry import normalize_vector
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        self.add_part(m.Part(name='part-1'))
        self.add_section(beam_section)

        for v in mesh.vertices():
            self.add_node(m.Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        vertices = list(mesh.vertices())
        edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

        for e in edges:
            # get elements orientation
            v = normalize_vector(mesh.edge_vector(e[0], e[1]))
            v.append(v.pop(0))
            # add element to the model
            self.add_element(m.BeamElement(connectivity=[
                             e[0], e[1]], section=beam_section.name, orientation=v), part='part-1')

    def shell_from_mesh(self, mesh, shell_section):
        """Creates a Model object from a compas Mesh object [WIP]. The faces of
        the mesh become the elements of the shell. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        mesh : obj
            Mesh to convert to import as a Model.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        self.add_part(m.Part(name='part-1'))
        self.add_section(shell_section)

        for v in mesh.vertices():
            self.add_node(m.Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        faces = [[key_index[key]
                  for key in mesh.face_vertices(face)] for face in mesh.faces()]

        for f in faces:
            self.add_element(m.ShellElement(connectivity=f, section=shell_section.name), part='part-1')

    def shell_from_gmesh(self, gmshModel, shell_section):
        """Creates a Model object from a gmsh Model object [WIP]. The faces of
        the mesh become the elements of the shell. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        gmshModel : obj
            gmsh Model to convert.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """

        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        self.add_part(m.Part(name='part-1'))
        self.add_section(shell_section)

        nodes = gmshModel.mesh.getNodes()
        node_tags = nodes[0]
        node_coords = nodes[1].reshape((-1, 3), order='C')
        for _, coords in zip(node_tags, node_coords):
            self.add_node(m.Node(coords.tolist()), 'part-1', check=False)
        elements = gmshModel.mesh.getElements()
        for etype, etags, ntags in zip(*elements):
            if etype == 2:
                for i, _ in enumerate(etags):
                    n = gmshModel.mesh.getElementProperties(etype)[3]
                    triangle = ntags[i * n: i * n + n]  # NOTE: seems pretty much useless
                    triangle = [x-1 for x in triangle]
                    self.add_element(m.ShellElement(connectivity=triangle, section=shell_section.name), part='part-1')

    def from_volmesh(self, volmesh):
        raise NotImplementedError()

    def from_solid(self, solid):
        raise NotImplementedError()

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def add_part(self, part, transformation={}):
        """Adds a Part to the Model and creates an Instance object from the
        specified Part and adds it to the Assembly. If a transformation matrix
        is specified, the instance is created in the transformed location.

        Parameters
        ----------
        part : obj
            Part object from which the Instance is created.
        transformation : dict
            Dictionary containing the transformation matrices to apply to the Part
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
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        if part.name in self.parts:
            print(
                "WARNING: Part {} already in the Model. Part not added!".format(part.name))
        else:
            self.parts[part.name] = part

        # TODO: implement transfromation operations
        if transformation:
            for i in transformation.keys():
                instance = self._instance_from_part(part, i, transformation[i])
                self.add_instance(instance)
        else:
            self.add_instance(m.Instance('{}-{}'.format(part.name, 1), part))

    def remove_part(self, part):
        """ Removes the part from the Model and all the referenced instances
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
        """Adds a compas_fea2 Instance object to the Model. If the Part to
        which the instance is referred to does not exist, it is automatically
        created.

        Warning
        -------
        Currently deprecated, because the creation of instances from the same
        part is less useful in a scripting context (where it is easy to generate
        already the parts in their correct locations). Maybe it will be useful in
        the future.

        Parameters
        ----------
        instance : obj
            compas_fea2 Instance object.

        Returns
        -------
        None
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        if instance.name not in self.instances:
            self.instances[instance.name] = instance
            if instance.part.name not in self.parts:
                self.parts[part.name] = instance.part
        else:
            print('Duplicate instance {} will be ignored!'.format(instance.name))

    def remove_instance(self, instance):
        """ Removes the part from the Model and all the referenced instances.

        Warning
        -------
        Currently deprecated. See `add_instance` for more details.

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
        raise NotImplementedError()

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def add_node(self, node, part, check=True):
        """Add a compas_fea2 `Node` object to a `Part` in the `Model`.
        If the `Node` object has no label, one is automatically assigned.
        Duplicate nodes are automatically excluded.

        Warning
        -------
        The part must have been previously added to the Model.


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

        if part in self.parts:
            self.parts[part].add_node(node, check)
        else:
            raise ValueError(
                '** ERROR! **: part {} not found in the Model!'.format(part))

    def add_nodes(self, nodes, part):
        """Add multiple compas_fea2 Node objects a Part in the Model.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are automatically excluded.
        The part must have been previously added to the Model.

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
        '''Remove the node from a Part in the Model. If there are duplicate nodes,
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

        if part in self.parts:
            self.parts[part].remove_node(node_key)
        else:
            raise ValueError(
                '** ERROR! **: part {} not found in the Model!'.format(part))

    def remove_nodes(self, nodes, part):
        '''Remove the nodes from a Part in the Model. If there are duplicate nodes,
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
        """Add a compas_fea2 `Element` object to a `Part` in the `Model`.

        Parameters
        ----------
        element : obj
            compas_fea2 `Element` object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        if part in self.parts:
            self.parts[part].add_element(element)
            if element.section not in self.sections:
                raise ValueError('ERROR: section {} not found in the Model!'.format(element.section))
            elif element.section not in self.parts[part].sections:
                self.parts[part].sections[element.section] = self.sections[element.section]
        else:
            raise ValueError('** ERROR! **: part {} not found in the Model!'.format(part))

    def add_elements(self, elements, part):
        """Adds multiple compas_fea2 Element objects to a Part in the Model.

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
        '''Removes the element from a Part in the Model.

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

        if part in self.parts:
            self.parts[part].remove_element(element_key)
        else:
            raise ValueError('ERROR: part {} not found in the Model!'.format(part))

    def remove_elements(self, elements, part):
        '''Removes the elements from a Part in the Model.

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
        raise NotImplementedError()

    def add_assembly_set(self, set, instance):
        '''Adds a Set object to the Model.

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
        if instance not in self.instances:
            raise ValueError('ERROR: instance {} not found in the Model!'.format(instance))
        set.instance = instance
        self.instances[instance].sets.append(set)

        self.sets[set.name] = set

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        '''Adds a Material object to the Model so that it can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            compas_fea2 material object.

        Returns
        -------
        None
        '''
        if material.name not in self.materials:
            self.materials[material.name] = material

    def add_materials(self, materials):
        '''Adds multiple Material objects to the Model so that they can be later refernced
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

    def assign_material_to_element(self, material, part, element):
        raise NotImplementedError()

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def add_section(self, section):
        """Adds a compas_fea2 Section object to the Model.

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

        if section.name not in self.sections:
            self.sections[section.name] = section
            if section.material not in self.materials.keys():
                raise ValueError('ERROR: material {} not found in the Model!'.format(
                    section.material))
            self.add_material(self.materials[section.material])

    def assign_section_to_element(self, material, part, element):
        raise NotImplementedError()

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

    def add_instance_set(self, iset, instance):
        """ Adds a set to a previously defined Instance.

        Parameters
        ----------
        part : obj
            Part object from which the Instance is created.
        transformation : matrix
            Trasformation matrix to apply to the Part before creating the Instance.
        """
        self.instances[instance].sets.append(iset)

    # =========================================================================
    #                        Interaction methods
    # =========================================================================

    def add_interactions(self, interactions):
        raise NotImplementedError()

    # =========================================================================
    #                          Helper methods
    # =========================================================================

    # TODO change to check through the instance

    def get_node_from_coordinates(self, xyz, tol):
        """Finds (if any) the Node object in the model with the specified coordinates.
        A tollerance factor can be specified.

        Parameters
        ----------
        xyz : list
            List with the [x, y, z] coordinates of the Node.
        tol : int
            multiple to which round the coordinates.

        Returns
        -------
        node : dict
            Dictionary with the Node object for each Instance.
            key =  Instance
            value = Node object with the specified coordinates.
        """

        node_dict = {}
        for part in self.parts.values():
            for node in part.nodes:

                a = [tol * round(i/tol) for i in node.xyz]
                b = [tol * round(i/tol) for i in xyz]
                # if math.isclose(node.xyz, xyz, tol):
                if a == b:
                    node_dict[part.name] = node.key

        if not node_dict:
            print("WARNING: Node at {} not found!".format(b))

        return node_dict

    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        """Prints a summary of the Model object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(self)

    # ==============================================================================
    # Save model file
    # ==============================================================================

    def save_to_cfm(self, path, output=True):
        """Exports the Model object to an .cfm file through Pickle.

        Parameters
        ----------
        path : path
            Path to the folder where save the file to.
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """

        if not os.path.exists(path):
            os.makedirs(path)

        filename = '{0}/{1}.cfm'.format(path, self.name)

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print('***** Model saved to: {0} *****\n'.format(filename))

    # ==============================================================================
    # Load model file
    # ==============================================================================

    @staticmethod
    def load_from_cfm(filename, output=True):
        """Imports a Model object from an .cfm file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Model .cfm from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Model object.
        """
        with open(filename, 'rb') as f:
            mdl = pickle.load(f)

        if output:
            print('***** Model loaded from: {0} *****'.format(filename))

        return mdl


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass