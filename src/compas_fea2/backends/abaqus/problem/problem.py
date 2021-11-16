from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from compas_fea2.backends._base.problem import ProblemBase

from compas_fea2.backends.abaqus.job.input_file import InputFile
from compas_fea2.backends.abaqus.job.input_file import ParFile
from compas_fea2.backends.abaqus.job.send_job import launch_process
from compas_fea2.backends.abaqus.job.send_job import launch_optimisation
from compas_fea2.backends.abaqus.problem.outputs import FieldOutput
from compas_fea2.backends.abaqus.problem.outputs import HistoryOutput
from compas_fea2.backends.abaqus.problem.steps import ModalStep

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Problem',
]


class Problem(ProblemBase):
    """Initialises the Problem object.

    Parameters
    ----------
    name : str
        Name of the Structure.
    model : obj
        model object.
    parts : list
        List of the parts in the model.

    Attributes
    ----------
    None
    """

    def __init__(self, name, model):
        super(Problem, self).__init__(name=name, model=model)
        self.parts = model.parts.values()  # TODO remove
        # self.interactions       = model.interactions

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def add_step(self, step):
        """Check if the Step parameters are correct and add a Step to the Problem.

        Parameters
        ----------
        step : obj
            compas_fea2 Step object.

        Returns
        -------
        None
        """

        # NOTE: the abaqus implementation is slightly different from the _base
        # TODO: simplify and move to _base

        if not step.__name__ == 'ModalCase':
            if step.displacements:
                for disp in step.displacements:
                    if disp not in self.displacements:
                        raise ValueError(
                            'ERROR: displacement {} not found in the model!'.format(disp))

            if step.loads:
                for load in step.loads:
                    if load not in self.loads:
                        raise ValueError('ERROR: load {} not found in the model!'.format(load))

            if not step.field_outputs:
                step.field_outputs = ['standard']
                self.field_outputs['standard'] = FieldOutput('standard')
            for fout in step.field_outputs:
                if fout not in self.field_outputs:
                    raise ValueError(
                        'ERROR: field output {} not found in the model!'.format(fout))

            if not step.history_outputs:
                step.history_outputs = ['standard']
                self.history_outputs['standard'] = HistoryOutput('standard')
            for hout in step.history_outputs:
                if hout not in self.history_outputs:
                    raise ValueError(
                        'ERROR: history output {} not found in the model!'.format(hout))

        self.steps[step.name] = step

    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    def set_optimisation_parameters(self, vf, iter_max, cpus):
        self.vf = vf
        self.iter_max = iter_max
        self.cpus = cpus

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    def write_input_file(self, output=True):
        """Writes the abaqus input file.

        Parameters
        ----------
        path : str
            Path to the folder where the input file will be saved.
        output : bool
            Print terminal output.
        save : bool
            Save problem to .cfp before file writing.

        Returns
        -------
        None

        """

        input_file = InputFile(self)
        r = input_file.write_to_file(self.path)
        if output:
            print(r)

    def write_parameters_file(self, output=True):
        """Writes the abaqus parameters file for the optimisation.

        Parameters
        ----------
        path : str
            Path to the folder where the input file will be saved.
        output : bool
            Print terminal output.
        save : bool
            Save structure to .cfp before file writing.

        Returns
        -------
        None

        """

        input_file = InputFile(self)
        inp = input_file.write_to_file(self.path)

        par_file = ParFile(self)
        par = par_file.write_to_file(self.path)

        if output:
            print(inp)
            print(par)

    # TODO: try to make this an abstract method of the base class
    def analyse(self, path='C:/temp', exe=None, cpus=1, output=True, overwrite=True, user_mat=False, save=False):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str
            Path to the folder where the input file is saved.
        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        output : bool
            Print terminal output.
        user_mat : str TODO: REMOVE!
            Name of the material defined through a subroutine (currently only one material is supported)
        save : bool
            Save structure to .cfp before file writing.

        Returns
        -------
        None

        """
        self.path = path if isinstance(path, Path) else Path(path)
        if not self.path.exists():
            self.path.mkdir()

        if save:
            self.save_to_cfp()

        self.write_input_file(output)
        launch_process(self, exe, output, overwrite, user_mat)

    def optimise(self, path='C:/temp', output=True, save=False):
        self.path = path if isinstance(path, Path) else Path(path)
        if not self.path.exists():
            self.path.mkdir()

        if save:
            self.save_to_cfp()

        self.write_input_file(output)
        self.write_parameters_file(output)
        launch_optimisation(self, output)


# =============================================================================
#                               Job data
# =============================================================================


    def _generate_jobdata(self):
        return f"""**
** BOUNDARY
**
{self._generate_bcs_section()}**
** STEPS
{self._generate_steps_section()}"""

    def _generate_bcs_section(self):
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
        for bc in self.bcs.values():
            section_data.append(bc._generate_jobdata())
        return ''.join(section_data)

    def _generate_steps_section(self):
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
        for step in self.steps.values():
            if isinstance(step, ModalStep):  # TODO too messy - check!
                section_data.append(step._generate_jobdata())
            else:
                section_data.append(step._generate_jobdata(self))

        return ''.join(section_data)


"""TODO: add cpu parallelization option
Parallel execution requested but no parallel feature present in the setup
"""

# =========================================================================
#                         Results methods
# =========================================================================

# # TODO: try to make this an abstract method of the base class
# def extract(self, fields='u', steps='all', exe=None, sets=None, license='research', output=True,
#             return_data=True, components=None):
#     """Extracts data from the analysis output files.

#     Parameters
#     ----------
#     fields : list, str
#         Data field requests.
#     steps : list
#         Loads steps to extract from.
#     exe : str
#         Full terminal command to bypass subprocess defaults.
#     sets : list
#         -
#     license : str
#         Software license type: 'research', 'student'.
#     output : bool
#         Print terminal output.
#     return_data : bool
#         Return data back into structure.results.
#     components : list
#         Specific components to extract from the fields data.

#     Returns
#     -------
#     None

#     """
#     extract_data(self, fields=fields, exe=exe, output=output, return_data=return_data,
#                  components=components)

# # this should be an abstract method of the base class
# def analyse_and_extract(self, fields='u', exe=None, cpus=4, license='research', output=True, save=False,
#                         return_data=True, components=None, user_mat=False, overwrite=True):
#     """Runs the analysis through the chosen FEA software / library and extracts data.

#     Parameters
#     ----------
#     fields : list, str
#         Data field requests.
#     exe : str
#         Full terminal command to bypass subprocess defaults.
#     cpus : int
#         Number of CPU cores to use.
#     license : str
#         Software license type: 'research', 'student'.
#     output : bool
#         Print terminal output.
#     save : bool
#         Save the structure to .obj before writing.
#     return_data : bool
#         Return data back into structure.results.
#     components : list
#         Specific components to extract from the fields data.
#     user_sub : bool
#         Specify the user subroutine if needed.
#     delete : bool
#         If True, the analysis results are deleted after being read. [Not Implemented yet]

#     Returns
#     -------
#     None

#     """

#     self.analyse(exe=exe, fields=fields, cpus=cpus, license=license, output=output, user_mat=user_mat,
#                 overwrite=overwrite, save=save)

#     self.extract(fields=fields, exe=exe, license=license, output=output,
#                 return_data=return_data, components=components)

# # this should be stored in a more generic way
# def get_nodal_results(self, step, field, nodes='all'):
#     """Extract nodal results from self.results.

#     Parameters
#     ----------
#     step : str
#         Step to extract from.
#     field : str
#         Data field request.
#     nodes : str, list
#         Extract 'all' or a node set/list.

#     Returns
#     -------
#     dict
#         The nodal results for the requested field.
#     """
#     data  = {}
#     rdict = self.results[step]['nodal']

#     if nodes == 'all':
#         keys = list(self.nodes.keys())
#     elif isinstance(nodes, str):
#         keys = self.sets[nodes].selection
#     else:
#         keys = nodes

#     for key in keys:
#         data[key] = rdict[field][key]

#     return data

# def get_element_results(self, step, field, elements='all'):
#     """Extract element results from self.results.

#     Parameters
#     ----------
#     step : str
#         Step to extract from.
#     field : str
#         Data field request.
#     elements : str, list
#         Extract 'all' or an element set/list.

#     Returns
#     -------
#     dict
#         The element results for the requested field.

#     """
#     data  = {}
#     rdict = self.results[step]['element']

#     if elements == 'all':
#         keys = list(self.elements.keys())
#     elif isinstance(elements, str):
#         keys = self.sets[elements].selection
#     else:
#         keys = elements

#     for key in keys:
#         data[key] = rdict[field][key]

#     return data
