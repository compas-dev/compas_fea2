from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
import importlib
from pathlib import Path

from compas_fea2.job.input_file import ParametersFile


class OptimisationProblem(FEAData):
    """General Optimisation Problem.

    Parameters
    ----------
    problem : obj
        :class:`compas_fea2.optimisation.Problem` subclass object.
    design_variables : obj
        :class:`compas_fea2.optimisation.DesignVariables` subclass object
    design_responses : dict
        dictionary with :class:`compas_fea2.optimisation.DesignResponse` subclass objects
    objective_function : obj
        :class:`compas_fea2.optimisation.ObectiveFunction` subclass object
    dv_constraints : dict of obj
        dict of :class:`compas_fea2.optimisation.OptimisationConstraint` subclass objects
    constraints : dict of obj
        dict of :class:`compas_fea2.optimisation.OptimisationConstraint` subclass objects
    strategy : str
        type of optimisation
    parameters : obj
        :class:`compas_fea2.optimisation.OptimisationParameters` subclass object.
    """

    def __init__(self, problem, design_variables, design_responses, objective_function,
                 dv_constraints, constraints, strategy, parameters, name=None, **kwargs):
        super(OptimisationProblem, self).__init__(name=name, **kwargs)
        self._problem = problem  # BUG this makes no sense...
        self._design_variables = design_variables
        self._design_responses = design_responses
        self._objective_function = objective_function
        self._dv_constraints = dv_constraints
        self._constraints = constraints
        self._strategy = strategy
        self._parameters = parameters

    @property
    def problem(self):
        """obj : :class:`compas_fea2.optimisation.Problem` subclass object."""
        return self._problem

    @property
    def desing_variables(self):
        """obj: :class:`compas_fea2.optimisation.DesignVariables` subclass object."""
        return self._desing_variables

    @property
    def desing_responses(self):
        """dict : dictionary with :class:`compas_fea2.optimisation.DesignResponse` subclass objects."""
        return self._desing_responses

    @property
    def objective_function(self):
        """obj : :class:`compas_fea2.optimisation.ObectiveFunction` subclass object."""
        return self._objective_function

    @property
    def dv_constraints(self):
        """dict : dict of :class:`compas_fea2.optimisation.OptimisationConstraint` subclass objects"""
        return self._dv_constraints

    @property
    def constraints(self):
        """dict : dict of :class:`compas_fea2.optimisation.OptimisationConstraint` subclass objects."""
        return self._constraints

    @property
    def strategy(self):
        """str : type of optimisation"""
        return self._strategy

    @property
    def parameters(self):
        """obj : :class:`compas_fea2.optimisation.OptimisationParameters` subclass object."""
        return self._parameters

    def add_objective_function(self, objective_function):
        raise NotImplementedError

    def add_design_response(self, design_response):
        raise NotImplementedError

    def add_constraint(self, constraint):
        raise NotImplementedError

    def write_parameters_file(self, path):
        """Writes the parameters file for the optimisation.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.

        Returns
        -------
        None
        """
        self.path = path
        if not self.path.exists():
            self.path.mkdir()
        par_file = ParametersFile.from_problem(self)
        return par_file.write_to_file(self.path)

    def solve(self, path, cpus=1, output=True, save=False, smooth=None):
        """Run Topology Optimisation procedure

        Warning
        -------
        ToscaStructure cannot read a model made of parts and assemblies. The model
        is automatically flatten and in case of incompatibilities, the names of
        nodes, elements and groups are automatically changed by the software. Check
        the input file automatically generated in the optimisation folder.

        Parameters
        ----------
        path : str, optional
            folder location where the optimisation results will be saved, by default 'C:/temp'
        cpus : int
            number of cpus used by the solver.
        output : bool, optional
            if ``True`` provides detailed output in the terminal, by default True
        save : bool, optional
            save results, by default False. CURRENTLY NOT IMPLEMENTED!
        smooth : obj, optional
            if a :class:`compas_fea2.optimisation.SmoothingParameters` subclass object is passed, the
            optimisation results will be postprocessed and smoothed, by defaut
            ``None`` (no smoothing)
        """
        self._path = path if isinstance(path, Path) else Path(path)
        self._problem._path = self._path
        if not self._path.exists():
            self._path.mkdir()
        if save:
            raise NotImplementedError
        self._problem.write_input_file(output)
        self.write_parameters_file(self._path, output, smooth)

    def smooth_optimisation(self, output):
        raise NotImplementedError


class TopOptSensitivity(OptimisationProblem):
    """Optimisation Problem for sensitivity-based topology optimisation.

    Parameters
    ----------
    problem : obj
        :class:`compas_fea2.optimisation.Problem` subclass object.
    design_variables : obj
        :class:`compas_fea2.optimisation.DesignVariables` subclass object
    vf : float
        volume fraction as final_volume/initial_volume
    lc : str
        load case from the FEA problem to consider in the optimisation problem [WIP]
    """

    def __init__(self, problem, design_variables, vf, lc, **kwargs):
        self._name = 'topology_optimisation_sesitivity'
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        dv_elements = m.DesignVariables('variables', design_variables)
        dr_volume = m.VolumeResponse(design_variables, 'sum')
        dr_energy = m.EnergyStiffnessResponse(design_variables, 'sum', lc)
        obj_function = m.ObjectiveFunction('min_compliance', dr_energy, 'MinMax')
        constraint = m.OptimisationConstraint('vol_frac', dr_volume, True)
        constraint <= vf
        parameters = m.OptimisationParameters(**kwargs)
        super(TopOptSensitivity, self).__init__(problem, dv_elements, {'v': dr_volume, 'se': dr_energy},
                                                obj_function, None, {'vf': constraint}, 'TOPO_SENSITIVITY', parameters)


class TopOptController(OptimisationProblem):
    pass
