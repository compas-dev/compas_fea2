from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
from compas_fea2.backends._base.job.input_file import InputFileBase
# from compas_fea2.backends.opensees.problem.steps import ModalStep
# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'InputFile',
]


class InputFile(InputFileBase):
    """Input file object for standard analysis.

    Parameters
    ----------
    problem : obj
        Problem object.

    Attributes
    ----------
    name : str
        Input file name.
    job_name : str
        Name of the Abaqus job. This is the same as the input file name.
    data : str
        Final input file text data that will be written in the .tcl file.
    """

    def __init__(self, problem):
        super(InputFile, self).__init__(problem)
        self._input_file_type = "Input File"
        self.name = '{}.tcl'.format(problem.name)
        self.data = self._generate_data(problem)

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _generate_data(self, problem):
        """Generate the content of the input fileself from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the input file
        """
        return """#------------------------------------------------------------------
# Heading
#------------------------------------------------------------------
#
{}
#
#
#------------------------------------------------------------------
# Nodes
#------------------------------------------------------------------
#
{}
#
#
#
#------------------------------------------------------------------
# Boundary conditions
#------------------------------------------------------------------
#
{}
#
#
#
#------------------------------------------------------------------
# Materials
#------------------------------------------------------------------
#
{}
#
#
#
#------------------------------------------------------------------
# Elements
#------------------------------------------------------------------
#
{}
#
#
#
#------------------------------------------------------------------
# Steps
#------------------------------------------------------------------
#
{}
#
#
#
# Output
#-------
#
{}
#
# Solver
#-------
#
#
{}
""".format()
# """.format(self.name, self.job_name, self._generate_part_section(problem), self._generate_assembly_section(problem),
#            self._generate_material_section(problem), self._generate_int_props_section(problem),
#            self._generate_interactions_section(problem), self._generate_bcs_section(problem),
#            self._generate_steps_section(problem))

    def _generate_part_section(self, problem):
        """Generate the content relatitive the each Part for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for part in problem.model.parts.values():
            data = part._generate_data()
            section_data.append(data)
        return ''.join(section_data)

    def _generate_assembly_section(self, problem):
        """Generate the content relatitive the assembly for the input file.

        Note
        ----
        in compas_fea2 the Model is for many aspects equivalent to an assembly in
        abaqus.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        return problem.model._generate_data()

    def _generate_material_section(self, problem):
        """Generate the content relatitive to the material section for the input
        file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for material in problem.model.materials.values():
            section_data.append(material.data)
        return ''.join(section_data)

    def _generate_int_props_section(self, problem):
        # # Write interaction properties
        # for interaction_property in problem.model.interaction_properties:
        #     interaction_property.write_data_line(f)
        return ''

    def _generate_interactions_section(self, problem):
        #
        # # Write interactions
        # for interaction in problem.model.interactions:
        #     interaction.write_data_line(f)
        return ''

    def _generate_bcs_section(self, problem):
        """Generate the content relatitive to the boundary conditions section
        for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for bc in problem.bcs.values():
            section_data.append(bc._generate_data())
        return ''.join(section_data)

    def _generate_steps_section(self, problem):
        """Generate the content relatitive to the steps section for the input
        file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for step in problem.steps:
            if isinstance(step, ModalStep):  # TODO too messy - check!
                section_data.append(step._generate_data())
            else:
                section_data.append(step._generate_data(problem))

        return ''.join(section_data)


if __name__ == "__main__":
    pass
