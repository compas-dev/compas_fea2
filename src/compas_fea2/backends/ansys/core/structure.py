
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from compas_fea.utilities import combine_all_sets
from compas_fea2.utilities import group_keys_by_attribute
from compas_fea2.utilities import group_keys_by_attributes

#TODO rmove useless imports
from compas_fea2._core.mixins.nodemixins import NodeMixins
from compas_fea2._core.mixins.elementmixins import ElementMixins
from compas_fea2._core.mixins.objectmixins import ObjectMixins
from compas_fea2._core import cStructure

# from compas_fea2._core.bcs import *
from compas_fea2.backends.abaqus.core import Set

from compas_fea2.backends.ansys.job.send_job import input_generate
from compas_fea2.backends.ansys.job.send_job import launch_process
from compas_fea2.backends.ansys.job.read_results import extract_rst_data

import pickle
import os


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
        'Structure',
        ]


class Structure(cStructure):

    def __init__(self, path, name='abaqus-Structure'):
        super(Structure, self).__init__(path, name)


    # ==============================================================================
    # Sets
    # ==============================================================================

    def add_set(self, name, type, selection):

        """ Adds a node, element or surface set to structure.sets.

        Parameters
        ----------
        name : str
            Name of the Set.
        type : str
            'node', 'element', 'surface_node', surface_element'.
        selection : list, dict
            The integer keys of the nodes, elements or the element numbers and sides.

        Returns
        -------
        None

        """

        if isinstance(selection, int):
            selection = [selection]

        self.sets[name] = Set(name=name, type=type, selection=selection, index=len(self.sets))


    def write_input_file(self, fields='u', output=True, save=False, ndof=6):

        """ Writes abaqus input file.

        Parameters
        ----------
        fields : list, str
            Data field requests.
        output : bool
            Print terminal output.
        save : bool
            Save structure to .obj before file writing.

        Returns
        -------
        None

        """

        if save:
            self.save_to_obj()

        input_generate(self) #TODO add fields


    def analyse(self, exe=None, cpus=4, license='research', delete=True, output=True):

        """ Runs the analysis through abaqus.

        Parameters
        ----------

        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        license : str
            Software license type: 'research', 'student'.
        delete : bool
            -
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """

        launch_process(self.path, self.name, cpus, license, delete=delete)


    def extract_data(self, fields='u', steps='all', exe=None, sets=None, license='research', output=True,
                     return_data=True, components=None):

        """ Extracts data from the analysis output files.

        Parameters
        ----------
        software : str
            Analysis software / library to use, 'abaqus', 'opensees' or 'ansys'.
        fields : list, str
            Data field requests.
        steps : list
            Loads steps to extract from.
        exe : str
            Full terminal command to bypass subprocess defaults.
        sets : list
            -
        license : str
            Software license type: 'research', 'student'.
        output : bool
            Print terminal output.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.

        Returns
        -------
        None

        """

        extract_rst_data(self, fields=fields, steps=steps, sets=sets, license=license)


    def analyse_and_extract(self, fields='u', exe=None, cpus=4, license='research', output=True, save=False,
                            return_data=True, components=None, ndof=6):

        """ Runs the analysis through the chosen FEA software / library and extracts data.

        Parameters
        ----------
        fields : list, str
            Data field requests.
        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        license : str
            Software license type: 'research', 'student'.
        output : bool
            Print terminal output.
        save : bool
            Save the structure to .obj before writing.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.

        Returns
        -------
        None

        """

        self.write_input_file(fields=fields, output=output, save=save, ndof=ndof)

        self.analyse(exe=exe, cpus=cpus, license=license, output=output)

        self.extract_data(fields=fields, exe=exe, license=license, output=output,
                          return_data=return_data, components=components)

