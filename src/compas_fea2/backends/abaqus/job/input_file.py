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

        self._jobdata = self._generate_jobdata()

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

    def _generate_jobdata(self):
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
        return """FEM_INPUT
  ID_NAME        = OPTIMIZATION_MODEL
  FILE           = {}
END_

DV_TOPO
  ID_NAME        = design_variables
  EL_GROUP       = ALL_ELEMENTS
END_

DRESP
  ID_NAME        = DRESP_SUM_ENERGY
  DEF_TYPE       = SYSTEM
  TYPE           = STRAIN_ENERGY
  UPDATE         = EVER
  EL_GROUP       = ALL_ELEMENTS
  GROUP_OPER     = SUM
END_

DRESP
  ID_NAME        = DRESP_VOL_TOPO
  DEF_TYPE       = SYSTEM
  TYPE           = VOLUME
  UPDATE         = EVER
  EL_GROUP       = ALL_ELEMENTS
  GROUP_OPER     = SUM
END_

OBJ_FUNC
  ID_NAME        = maximize_stiffness
  DRESP          = DRESP_SUM_ENERGY
  TARGET         = MINMAX
END_

CONSTRAINT
  ID_NAME        = volume_constraint
  DRESP          = DRESP_VOL_TOPO
  MAGNITUDE      = REL
  EQ_VALUE       = {}
END_

OPTIMIZE
  ID_NAME        = topology_optimization
  DV             = design_variables
  OBJ_FUNC       = maximize_stiffness
  CONSTRAINT     = volume_constraint
  STRATEGY       = TOPO_CONTROLLER
END_

OPT_PARAM
  ID_NAME = topology_optimization_OPT_PARAM_
  OPTIMIZE = topology_optimization
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
  ITER_MAX       = {}
END_

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
END_""".format(self.input_name, self.vf, self.iter_max)
