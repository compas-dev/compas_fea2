from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas_fea2.results.results import (
    DisplacementResult,
    SectionForcesResult,
    ReactionResult,
    VelocityResult,
    AccelerationResult,
    ShellStressResult,
)
from compas_fea2.results.database import ResultsDatabase


class _Output(FEAData):
    """Base class for output requests.

    Parameters
    ----------
    FEAData : _type_
        _description_

    Notes
    -----
    Outputs are registered to a :class:`compas_fea2.problem.Step`.

    """

    def __init__(self, results_cls, **kwargs):
        super(_Output, self).__init__(**kwargs)
        self._results_cls = results_cls

    @property
    def results_cls(self):
        return self._results_cls

    @property
    def sqltable_schema(self):
        return self._results_cls.sqltable_schema()

    @property
    def results_func(self):
        return self._results_cls._results_func

    @property
    def field_name(self):
        return self.results_cls._field_name

    @property
    def components_names(self):
        return self.results_cls._components_names

    @property
    def invariants_names(self):
        return self.results_cls._invariants_names

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step.problem

    @property
    def model(self):
        return self.problem.model

    def create_sql_table(self, connection, results):
        """
        Delegate the table creation to the ResultsDatabase class.
        """
        ResultsDatabase.create_table_for_output_class(self, connection, results)


class _NodeFieldOutput(_Output):
    """NodeFieldOutput object for requesting the fields at the nodes from the analysis."""

    def __init__(self, results_cls, **kwargs):
        super().__init__(results_cls=results_cls, **kwargs)


class DisplacementFieldOutput(_NodeFieldOutput):
    """DisplacmentFieldOutput object for requesting the displacements at the nodes
    from the analysis."""

    def __init__(self, **kwargs):
        super(DisplacementFieldOutput, self).__init__(DisplacementResult, **kwargs)


class AccelerationFieldOutput(_NodeFieldOutput):
    """AccelerationFieldOutput object for requesting the accelerations at the nodes
    from the analysis."""

    def __init__(self, **kwargs):
        super(AccelerationFieldOutput, self).__init__(AccelerationResult, **kwargs)


class VelocityFieldOutput(_NodeFieldOutput):
    """VelocityFieldOutput object for requesting the velocities at the nodes
    from the analysis."""

    def __init__(self, **kwargs):
        super(VelocityFieldOutput, self).__init__(VelocityResult, **kwargs)


class ReactionFieldOutput(_NodeFieldOutput):
    """ReactionFieldOutput object for requesting the reaction forces at the nodes
    from the analysis."""

    def __init__(self, **kwargs):
        super(ReactionFieldOutput, self).__init__(ReactionResult, **kwargs)


class _ElementFieldOutput(_Output):
    """ElementFieldOutput object for requesting the fields at the elements from the analysis."""

    def __init__(self, results_cls, **kwargs):
        super().__init__(results_cls=results_cls, **kwargs)


class Stress2DFieldOutput(_ElementFieldOutput):
    """StressFieldOutput object for requesting the stresses at the elements from the analysis."""

    def __init__(self, **kwargs):
        super(Stress2DFieldOutput, self).__init__(ShellStressResult, **kwargs)


class SectionForcesFieldOutput(_ElementFieldOutput):
    """SectionForcesFieldOutput object for requesting the section forces at the elements from the analysis."""

    def __init__(self, **kwargs):
        super(SectionForcesFieldOutput, self).__init__(SectionForcesResult, **kwargs)


class HistoryOutput(_Output):
    """HistoryOutput object for recording the fields (stresses, displacements,
    etc..) from the analysis.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    """

    def __init__(self, **kwargs):
        super(HistoryOutput, self).__init__(**kwargs)
