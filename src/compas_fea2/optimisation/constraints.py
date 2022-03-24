from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class OptimisationConstraint(FEAData):
    """Define an optimisation constraint.

    Note
    ----
    Constraints can be set by simply using the ``==, >=, <=`` operators.

    Note
    ----
    In topology optimization the start model for the optimization is the model used
    for the first finite element analysis in the optimization procedure (iteration 0).
    The element densities might differ from the initial model (e.g. when no
    volume constraint is present they are set to 50% of the original density).
    Take this into account when defining, e.g., relative displacement or frequency
    onstraints. This behavior can be controlled by the user with the parameter
    ``DENSITY_INITIAL`` in the :class:`OptimisationParameters` command.

    Warning
    -------
    Inequality constraints can only be used for the `sensitivity-based` optimizations.
    Equality constraints can be used only for `controller-based` optimisations.

    Parameters
    ----------
    name : str
        name of the constraint
    design_response : obj
        :class:`compas_fea2.optimisation.DesignResponse` subclass object of the desing response to constraint
    relative : bool
        if ``True`` the constraint is set relatively to the initial value of the
        desing response. Relative values always refer to the design response of
        the start model for the optimization. Example: The relative value 0.8 represents 80%

    Example
    -------
    >>> constraint = OptimisationConstraint('vol_frac', dr_volume, True)
    >>> constraint <= 0.3

    """

    def __init__(self, name, design_response, relative=False) -> None:
        self._name = name
        self._design_response = design_response
        self._relative = relative
        self._constraint_type = None
        self._constraint_value = None

    def __eq__(self, __o: object):
        self._constraint_type = '='
        self._constraint_value = __o

    def __ge__(self, __o: object):
        self._constraint_type = '>='
        self._constraint_value = __o

    def __le__(self, __o: object):
        self._constraint_type = '<='
        self._constraint_value = __o

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def name(self):
        """str : name of the constraint."""
        return self._name

    @property
    def design_response(self):
        """obj : :class:`compas_fea2.optimisation.DesignResponse` subclass object of the desing response to constraint."""
        return self._design_response

    @property
    def relative(self):
        """bool : if ``True`` the constraint is set relatively to the initial value of the
        desing response."""
        return self._relative

    @property
    def constraint_type(self):
        """The constraint_type property."""
        return self._constraint_type

    @property
    def constraint_value(self):
        """The constraint_value property."""
        return self._constraint_value
