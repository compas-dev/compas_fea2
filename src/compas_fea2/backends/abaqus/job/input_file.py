from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import compas_fea2
from compas_fea2.job import InputFile
from compas_fea2.job.input_file import ParametersFile


class AbaqusInputFile(InputFile):
    """"""

    def __init__(self, name=None, **kwargs):
        super(AbaqusInputFile, self).__init__(name=name, **kwargs)
        self._extension = 'inp'

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _generate_jobdata(self):
        """Generate the content of the input file from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return """*Heading
** Job name: {}
** Generated using compas_fea2 version {}
** Author: {}
** Date: {}
** Model Description : {}
** Problem Description : {}
**
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**
**------------------------------------------------------------------
**------------------------------------------------------------------
** MODEL
**------------------------------------------------------------------
**------------------------------------------------------------------
**
{}**
**------------------------------------------------------------------
**------------------------------------------------------------------
** PROBLEM
**------------------------------------------------------------------
**------------------------------------------------------------------
{}""".format(self._job_name, compas_fea2.__version__,
             self.model.author,
             now,
             self.model.description,
             self.problem.description,
             self.model._generate_jobdata(),
             self.problem._generate_jobdata())


class AbaqusRestartInputFile(InputFile):
    """"""

    def __init__(self, start, steps, name=None, **kwargs):
        super(AbaqusRestartInputFile, self).__init__(name=name, **kwargs)
        self._extension = 'inp'
        self._start = start
        self._steps = steps

    @property
    def start(self):
        return self._start

    @property
    def steps(self):
        return self._steps

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    @classmethod
    def from_problem(cls, problem, start, steps):
        """Create an AbaqusRestartInputFile object from a :class:`compas_fea2.problem.Problem`,
        a starting increment and and additional steps

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            Problem to be converted to InputFile.

        Returns
        -------
        obj
            InputFile for the analysis.
        """
        restart_file = cls(start=start, steps=steps)
        restart_file._registration = problem
        restart_file._job_name = problem.name+'_restart'
        restart_file._file_name = '{}.{}'.format(restart_file._job_name, restart_file._extension)

        return restart_file

    def _generate_jobdata(self):
        """Generate the content of the input file from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return """*Heading
** Job name: {}
** Generated using compas_fea2 version {}
** Author: {}
** Date: {}
** Model Description : {}
** Problem Description : {}
**
*Restart, read, step={}
**
**------------------------------------------------------------------
**------------------------------------------------------------------
** ADDITIONAL STEPS
**------------------------------------------------------------------
**------------------------------------------------------------------
{}""".format(self._job_name, compas_fea2.__version__,
             self.model.author,
             now,
             self.model.description,
             self.problem.description,
             self.start,
             '\n'.join([step._generate_jobdata() for step in self.steps]))


class AbaqusParametersFile(ParametersFile):
    """"""

    def __init__(self, name=None, **kwargs):
        super(AbaqusParametersFile, self).__init__(name, **kwargs)
        self._extension = 'par'

    @classmethod
    def from_problem(cls, problem, smooth):
        """[summary]

        Parameters
        ----------
        problem : obj
            :class:`compas_fea2.problem.Problem` sub class object.
        smooth : obj, optional
            if a :class:`compas_fea2.optimisation.SmoothingParameters` subclass object is passed, the
            optimisation results will be postprocessed and smoothed, by defaut
            ``None`` (no smoothing)

        Returns
        -------
        obj
            InputFile for the analysis.
        """
        input_file = cls()
        input_file._job_name = problem._name
        input_file._file_name = '{}.{}'.format(problem._name, input_file._extension)
        input_file._job_data = input_file._generate_jobdata(problem, smooth)
        input_file._registration = problem
        return input_file

    def _generate_jobdata(self, opti_problem, smooth):
        """Generate the content of the parameter file from the optimisation
        settings of the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the .par file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""! Optimization Process name: {self._job_name}
! Model name: {opti_problem._problem.model.name}
! Task name: TopOpt
! Generated using compas_fea2 version {compas_fea2.__version__}
! Author: {opti_problem._problem.author}
! Date: {now}
!
! ----------------------------------------------------------------
! Input model
!
FEM_INPUT
  ID_NAME        = OPTIMIZATION_MODEL
  FILE           = {opti_problem._problem._name}.inp
END_
!
! ----------------------------------------------------------------
! Design area
{opti_problem._design_variables._generate_jobdata()}!
! ----------------------------------------------------------------
! Design responses
{''.join([value._generate_jobdata() for value in opti_problem._design_responses.values()])}!
! ----------------------------------------------------------------
! Objective Function
{opti_problem._objective_function._generate_jobdata()}!
! ----------------------------------------------------------------
! Constraints
{''.join([value._generate_jobdata() for value in opti_problem._constraints.values()])}!
! ----------------------------------------------------------------
! Task
{opti_problem._generate_jobdata()}!
! ----------------------------------------------------------------
! Parameters
{opti_problem._parameters._generate_jobdata(opti_problem._name)}!
!
! ----------------------------------------------------------------
!
{smooth._generate_jobdata() if smooth else '!'}
EXIT"""
