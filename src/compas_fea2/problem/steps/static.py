from .step import GeneralStep


class StaticStep(GeneralStep):
    """StaticStep for use in a static analysis.

    Parameters
    ----------
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.
    loads : dict
        Dictionary of the loads assigned to each part in the model in the step.
    displacements : dict
        Dictionary of the displacements assigned to each part in the model in the step.

    """

    def __init__(
        self,
        max_increments=100,
        initial_inc_size=1,
        min_inc_size=0.00001,
        max_inc_size=1,
        time=1,
        nlgeom=False,
        modify=True,
        **kwargs,
    ):
        super().__init__(
            max_increments=max_increments,
            initial_inc_size=initial_inc_size,
            min_inc_size=min_inc_size,
            max_inc_size=max_inc_size,
            time=time,
            nlgeom=nlgeom,
            modify=modify,
            **kwargs,
        )

    @property
    def __data__(self):
        return {
            "max_increments": self.max_increments,
            "initial_inc_size": self.initial_inc_size,
            "min_inc_size": self.min_inc_size,
            "time": self.time,
            "nlgeom": self.nlgeom,
            "modify": self.modify,
            # Add other attributes as needed
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            max_increments=data["max_increments"],
            initial_inc_size=data["initial_inc_size"],
            min_inc_size=data["min_inc_size"],
            time=data["time"],
            nlgeom=data["nlgeom"],
            modify=data["modify"],
            # Add other attributes as needed
        )


class StaticRiksStep(StaticStep):
    """Step for use in a static analysis when Riks method is necessary."""

    def __init__(
        self,
        max_increments=100,
        initial_inc_size=1,
        min_inc_size=0.00001,
        time=1,
        nlgeom=False,
        modify=True,
        **kwargs,
    ):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, **kwargs)
        raise NotImplementedError
