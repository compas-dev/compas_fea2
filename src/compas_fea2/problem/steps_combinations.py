from compas_fea2.base import FEAData


class StepsCombination(FEAData):
    """A StepsCombination `sums` the analysis results of given steps
    (:class:`compas_fea2.problem.LoadPattern`).

    Parameters
    ----------
    FEAData : _type_
        _description_

    Notes
    -----
    By default every analysis in `compas_fea2` is meant to be `non-linear`, in
    the sense that the effects of a load pattern (:class:`compas_fea2.problem.Pattern`)
    in a given steps are used as a starting point for the application of the load
    patterns in the next step. Therefore, the sequence of the steps can affect
    the results (if the response is actully non-linear).

    """

    def __init__(self, **kwargs):
        raise NotImplementedError()
