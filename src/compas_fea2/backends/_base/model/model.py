from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import math
import pickle

from ..base import FEABase


__all__ = ['ModelBase']


class ModelBase(FEABase):
    """Base class for models.

    Parameters
    ----------
    name: str
        Name of the Model.

    Attributes
    ----------
    name: str
        Name of the Model.
    parts : dict
        A dictionary with the Part objects referenced in the Model.
    materials : dict
        A dictionary of all the materials defined in the Model.
    sections : dict
        A dictionary of all the sections defined in the Model.
    sets : dict
        A dictionary of all the sets defined in the Model.
    """

    def __init__(self, name):
        self.name = name
        self.parts = {}
        self.materials = {}
        self.sections = {}
        self.sets = {}

    # def __str__(self):
    #     title = 'compas_fea2 {0} object'.format(self.__name__)
    #     separator = '-' * (len(self.__name__) + 19)
    #     data = []
    #     for attr in ['name']:
    #         data.append('{0:<15} : {1}'.format(attr, getattr(self, attr)))

    #     data.append('{0:<15} : {1}'.format('# of parts', len(self.parts)))
    #     data.append('{0:<15} : {1}'.format(
    #         '# of instances', len(self.instances)))
    #     return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(data))

    def summary(self):
        """Print a summary of the Model object.
        """
        print(self)

    # =========================================================================
    # Parts methods
    # =========================================================================

    def add_part(self, part):
        """Add a part to the model.

        Parameters
        ----------
        part :
            Part object from which the Instance is created.

        Returns
        -------
        None

        Examples
        --------
        In this example a part is added to the model and two instances are created
        using two transformation matrices.

        >>> model = Model('mymodel')
        >>> part = Part('mypart')
        >>> model.add_part(part=part)

        """
        if part.name in self.parts:
            print("WARNING: Part {} already exists in the Model. Part not added!".format(part.name))
        else:
            self.parts[part.name] = part

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
        if part.name in self.parts:
            del self.parts[part.name]

    # =========================================================================
    # Instances methods
    # =========================================================================

    # =========================================================================
    # Nodes methods
    # =========================================================================

    # =========================================================================
    # Elements methods
    # =========================================================================

    # def add_element(self, element, part):
    #     """Adds a compas_fea2 Element object to a Part in the Model.

    #     Parameters
    #     ----------
    #     element : obj
    #         compas_fea2 Element object.
    #     part : str
    #         Name of the part where the nodes will be removed from.

    #     Returns
    #     -------
    #     None
    #     """
    #     error_code = 0
    #     if part in self.parts:
    #         self.parts[part].add_element(element)
    #         if element.section not in self.sections:
    #             sys.exit('ERROR: section {} not found in the Model!'.format(element.section))
    #         elif element.section not in self.parts[part].sections:
    #             self.parts[part].sections[element.section] = self.sections[element.section]
    #         error_code = 1

    #     if error_code == 0:
    #         sys.exit('ERROR: part {} not found in the Model!'.format(part))

    # def remove_element(self, element_key, part):
    #     '''Removes the element from a Part in the Model.

    #     Parameters
    #     ----------
    #     element_key : int
    #         Key number of the element to be removed.
    #     part : str
    #         Name of the part where the nodes will be removed from.

    #     Returns
    #     -------
    #     None
    #     '''
    #     error_code = 0
    #     if part in self.parts:
    #         self.parts[part].remove_element(element_key)
    #         error_code = 1

    #     if error_code == 0:
    #         sys.exit('ERROR: part {} not found in the Model!'.format(part))

    # =========================================================================
    # Sets methods
    # =========================================================================

    # =========================================================================
    # Materials methods
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

    # =========================================================================
    # Sections methods
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
                sys.exit('ERROR: material {} not found in the Model!'.format(
                    section.material))
            self.add_material(self.materials[section.material])

    # =========================================================================
    # Surfaces methods
    # =========================================================================

    # =========================================================================
    # Constraints methods
    # =========================================================================

    # =========================================================================
    # Interaction methods
    # =========================================================================

    # =========================================================================
    # Helper methods
    # =========================================================================

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
