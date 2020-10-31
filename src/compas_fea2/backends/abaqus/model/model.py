from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

import os
import sys
import math
import pickle

from compas_fea2.backends._base.model import ModelBase

__all__ = [
    'Model',
]


class Model(ModelBase):
    """Initialises the Model object. This is in many aspects equivalent to an
    `Assembly` in Abaqus.

    Parameters
    ----------
    name : str
        Name of the Model.

    Attributes
    ----------
    name : str
        Name of the Model.
    parts : list
        A list with the Part objects referenced in the Model.
    instances : dict
        A dictionary with the Instance objects belonging to the Model.
    parts : dict
        A dictionary with the Part objects referenced in the Model.
    surfaces : list
        A list with the Surface objects belonging to the Model.
    constraints : list
        A list with the Constraint objects belonging to the Model.
    materials : dict
        A dictionary of all the materials defined in the Model.
    sections : dict
        A dictionary of all the sections defined in the Model.
    sets : dict
        A dictionary of all the sets defined in the Model.
    """

    def __init__(self, name):
        super(Model, self).__init__(name)
        self._backend = 'abaqus'

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

    def from_network(self, network):
        pass

    def from_obj(self, obj):
        pass

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

        from compas_fea2.backends.abaqus.model import Node
        from compas_fea2.backends.abaqus.model import Part
        from compas_fea2.backends.abaqus.model import BeamElement

        self.add_part(Part(name='part-1'))
        self.add_section(beam_section)

        for v in mesh.vertices():
            self.add_node(Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        vertices = list(mesh.vertices())
        edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

        for e in edges:
            # get elements orientation
            v = normalize_vector(mesh.edge_vector(e[0], e[1]))
            v.append(v.pop(0))
            # add element to the model
            self.add_element(BeamElement(connectivity=[
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
        from compas.geometry import normalize_vector

        from compas_fea2.backends.abaqus.model import Node
        from compas_fea2.backends.abaqus.model import Part
        from compas_fea2.backends.abaqus.model import ShellElement

        self.add_part(Part(name='part-1'))
        self.add_section(shell_section)

        for v in mesh.vertices():
            self.add_node(Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        faces = [[key_index[key]
                  for key in mesh.face_vertices(face)] for face in mesh.faces()]

        for f in faces:
            self.add_element(ShellElement(
                connectivity=f, section=shell_section.name), part='part-1')

    def from_volmesh(self, volmesh):
        pass

    def from_solid(self, solid):
        pass

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

        from compas_fea2.backends.abaqus.model import Instance

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
            self.add_instance(Instance('{}-{}'.format(part.name, 1), part))

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

        Parameters
        ----------
        instance : obj
            compas_fea2 Instance object.

        Returns
        -------
        None
        """

        if instance.name not in self.instances:
            self.instances[instance.name] = instance
            if instance.part.name not in self.parts:
                self.parts[part.name] = instance.part
        else:
            print('Duplicate instance {} will be ignored!'.format(instance.name))

    def remove_instance(self, instance):
        """ Removes the part from the Model and all the referenced instances.

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


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
