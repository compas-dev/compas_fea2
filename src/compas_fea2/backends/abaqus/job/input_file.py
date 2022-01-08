from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import compas_fea2
import os.path
from compas_fea2.backends._base.job.input_file import InputFileBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'InputFile',
    'ParFile'
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

    """

    def __init__(self, problem):
        super(InputFile, self).__init__(problem)
        self._input_file_type = "Input File"
        self._name = '{}.inp'.format(problem.name)
        self._jobdata = self._generate_jobdata(problem)

    @property
    def name(self):
        """The name property."""
        return self._name

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        return self._jobdata

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _generate_jobdata(self, problem):
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
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""** {self._name}
*Heading
** Job name: {self._job_name}
** Generated using compas_fea2 version {compas_fea2.__version__}
** Author: {problem.author}
** Date: {now}
**
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**
**------------------------------------------------------------------
**------------------------------------------------------------------
** MODEL
**------------------------------------------------------------------
**------------------------------------------------------------------
**
{problem.model._generate_jobdata()}
**------------------------------------------------------------------
**------------------------------------------------------------------
** PROBLEM
**------------------------------------------------------------------
**------------------------------------------------------------------
{problem._generate_jobdata()}"""


class ParFile(InputFileBase):
    """ParFile object for optimisation.

    Parameters
    ----------
    problem : obj
        Problem object.

    Attributes
    ----------
    name : str
        Par file name.
    job_name : str
        Name of the Abaqus job. This is the same as the input file name.
    """

    def __init__(self, problem):
        super(ParFile, self).__init__(problem)
        self._input_file_type = "Parameters File"
        self.name = '{}.par'.format(problem.name)
        self.input_name = '{}.inp'.format(problem.name)
        self.vf = problem.vf
        self.iter_max = problem.iter_max
        self._jobdata = self._generate_jobdata(problem)

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        return self._jobdata

    def _generate_jobdata(self, problem):
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
! Model name: {problem.model.name}
! Task name: TopOpt
! Generated using compas_fea2 version {compas_fea2.__version__}
! Author: {problem.author}
! Date: {now}
!
! ----------------------------------------------------------------
! Input model
!
FEM_INPUT
  ID_NAME        = OPTIMIZATION_MODEL
  FILE           = {self.input_name}
END_
!
! ----------------------------------------------------------------
! Design area for task: top_opt
!
DV_TOPO
  ID_NAME        = top_opt_DESIGN_AREA_
  EL_GROUP       = ALL_ELEMENTS
END_
!
! ----------------------------------------------------------------
! Design Response: strain_eng
!
DRESP
  ID_NAME        = strain_eng
  DEF_TYPE       = SYSTEM
  TYPE           = ENERGY_STIFF_MEASURE
  UPDATE         = EVER
  EL_GROUP       = ALL_ELEMENTS
  GROUP_OPER     = SUM
  LC_SET         = ALL, 1, ALL
END_
!
! ----------------------------------------------------------------
! Design Response: volume
!
DRESP
  ID_NAME        = volume
  DEF_TYPE       = SYSTEM
  TYPE           = VOLUME
  UPDATE         = EVER
  EL_GROUP       = ALL_ELEMENTS
  GROUP_OPER     = SUM
END_
!
! ----------------------------------------------------------------
! Objective Function: maximize_stiffness
!
OBJ_FUNC
  ID_NAME        = maximize_stiffness
  DRESP          = strain_eng, 1
  TARGET         = MINMAX
END_
!
! ----------------------------------------------------------------
! Constraint: vol_fraction
!
CONSTRAINT
  ID_NAME        = vol_fraction
  DRESP          = volume
  MAGNITUDE      = REL
  EQ_VALUE       = {self.vf}
END_
!
! ----------------------------------------------------------------
! Task: top_opt
!
OPTIMIZE
  ID_NAME        = top_opt
  DV             = top_opt_DESIGN_AREA_
  OBJ_FUNC       = maximize_stiffness
  CONSTRAINT     = vol_fraction
  STRATEGY       = TOPO_SENSITIVITY
END_
OPT_PARAM
  ID_NAME = top_opt_OPT_PARAM_
  OPTIMIZE = top_opt
  AUTO_FROZEN = LOAD
  DENSITY_UPDATE = NORMAL
  DENSITY_LOWER = 0.001
  DENSITY_UPPER = 1.
  DENSITY_MOVE = 0.25
  MAT_PENALTY = 3.
  STOP_CRITERION_LEVEL = BOTH
  STOP_CRITERION_OBJ = 0.001
  STOP_CRITERION_DENSITY = 0.005
  STOP_CRITERION_ITER = 4
  SUM_Q_FACTOR = 6.
END_
STOP
  ID_NAME        = global_stop
  ITER_MAX       = {self.iter_max}
END_
!
! ----------------------------------------------------------------
!
SMOOTH
  id_name = ISO_SMOOTHING_0_3
  task = iso
  iso_value = 0.3
  SELF_INTERSECTION_CHECK = runtime
  smooth_cycles = 10
  reduction_rate = 60
  reduction_angle = 5.0
  format = vtf
  format = stl
  format = onf
END_
DRIVER
driver.Solver.AddCallArgs = ['message', 'messaging_mechanism=DIRECT', 'listener_name=FR-lenovo-P52', 'listener_resource=40212', 'direct_port=64475',  'memory=90%', 'cpus=4',]
config.registerSaveRule(UpdateRules.MOVE, CheckPoints.CYCLE_COMPLETE, EventTimes.NEVER, [ '*.odb' ], 'SAVE.odb')
config.registerSaveRule(UpdateRules.COPY, CheckPoints.CYCLE_COMPLETE, EventTimes.EVER, [ '*.odb' ], 'SAVE.odb', '_%i')
config.registerSaveRule(UpdateRules.COPY, CheckPoints.CYCLE_COMPLETE, EventTimes.EVER, [ '*.msg' ], 'SAVE.msg', '_%i')
config.registerSaveRule(UpdateRules.COPY, CheckPoints.CYCLE_COMPLETE, EventTimes.EVER, [ '*.dat' ], 'SAVE.dat', '_%i')
config.registerSaveRule(UpdateRules.COPY, CheckPoints.CYCLE_COMPLETE, EventTimes.EVER, [ '*.sta' ], 'SAVE.sta', '_%i')
driver.registerCheckPointHook(CheckPoints.ITER_COMPLETE, HookTypes.POST, EventTimes.EVER, [ driver.Solver.Path, 'python', '-m', 'driverWriteOnfToOdb', '--type', OptimizationTypes.toOnf(driver.OptimizationType), '--inp', SMATsoUtil.basename(driver.FemInput.MasterFile) ], True, silent=True)
driver.Solver.RemoveUserRequests = False
END_
EXIT"""
