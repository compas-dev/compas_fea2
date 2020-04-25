
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2._core import cStructure

from compas_fea2.backends.abaqus.core.mixins.nodemixins import NodeMixins
from compas_fea2.backends.abaqus.core.mixins.elementmixins import ElementMixins
from compas_fea2.backends.abaqus.core.mixins.objectmixins import ObjectMixins

# from compas_fea2.backends.abaqus.core import Set #TODO remove!

from compas_fea2.backends.opensees.job import input_generate
from compas_fea2.backends.opensees.job import launch_process
from compas_fea2.backends.opensees.job import get_data



# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
        'Structure',
        ]


class Structure(cStructure, ObjectMixins, ElementMixins, NodeMixins):

    def __init__(self, path, name='opensees-Structure'):
        super(Structure, self).__init__(path, name)

    # #TODO remove
    # def add_set(self, name, type, selection):

    #     """ Adds a node, element or surface set to structure.sets.

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

    def write_input_file(self, fields='u', output=True, save=False, ndof=6):

        """ Writes opensees input file.

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
            self.save_to_cfea()

        input_generate(self, fields=fields, output=output, ndof=ndof)


    def analyse(self, exe=None, output=True):

        """ Runs the analysis through opensees.

        Parameters
        ----------

        exe : str
            Full terminal command to bypass subprocess defaults.

        output : bool
            Print terminal output.

        Returns
        -------
        None

        """

        launch_process(self, exe=exe, output=output)


    def extract_data(self, fields='u'):

        """ Extracts data from the analysis output files.

        Parameters
        ----------
        fields : list, str
            Data field requests.

        Returns
        -------
        None

        """

        get_data(self, fields=fields)

    def analyse_and_extract(self, fields='u', exe=None, output=True, save=False, ndof=6):

        """ Runs the analysis through opensees and extracts data.

        Parameters
        ----------
        fields : list, str
            Data field requests
        exe : str
            Full terminal command to bypass subprocess defaults.
        output : bool
            Print terminal output.
        save : bool
            Save the structure to .cfea before writing.

        Returns
        -------
        None

        """

        self.write_input_file(fields=fields, output=output, save=save, ndof=ndof)

        self.analyse(exe=exe, output=output)

        self.extract_data(fields=fields, exe=exe, output=output)

