from .step import GeneralStep


class QuasiStaticStep(GeneralStep):
    """Step for quasi-static analysis."""

    def __init__(self, **kwargs):
        super(QuasiStaticStep, self).__init__(**kwargs)
        raise NotImplementedError

    @property
    def __data__(self):
        data = super().__data__
        # Add specific data for QuasiStaticStep
        return data

    @classmethod
    def __from_data__(cls, data):
        obj = super(QuasiStaticStep, cls).__from_data__(data)
        # Initialize specific attributes for QuasiStaticStep
        return obj


class DirectCyclicStep(GeneralStep):
    """Step for a direct cyclic analysis."""

    def __init__(self, **kwargs):
        super(DirectCyclicStep, self).__init__(**kwargs)
        raise NotImplementedError

    @property
    def __data__(self):
        data = super().__data__
        # Add specific data for DirectCyclicStep
        return data

    @classmethod
    def __from_data__(cls, data):
        obj = super(DirectCyclicStep, cls).__from_data__(data)
        # Initialize specific attributes for DirectCyclicStep
        return obj
