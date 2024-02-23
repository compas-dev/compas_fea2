from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

class LoadCombination(FEAData):
    """Load combination object used to combine patterns together at each step.

    Parameters
    ----------
    factors : dict()
        Dictionary with the factors for each load case: {"load case": factor}
    name : str, optional
        Name to assign to the combination,  by default None (automatically assigned).

    """
    def __init__(self, factors, name=None, **kwargs):
        super(LoadCombination, self).__init__(name, **kwargs)
        self.factors=factors

    @property
    def load_cases(self):
        for k in self.factors.keys():
            yield k

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step._registration

    @property
    def model(self):
        self.problem._registration

    @classmethod
    def ULS(cls):
        return cls(factors={"DL":1.35, "SDL":1.35, "LL":1.35}, name="ULS")

    @classmethod
    def SLS(cls):
        return cls(factors={"DL":1, "SDL":1, "LL":1}, name="ULS")

    @classmethod
    def Fire(cls):
        return cls(factors={"DL":1, "SDL":1, "LL":0.3}, name="Fire")

    @property
    def node_load(self):
        """Generator returning each node and the correponding total factored
        load of the combination.

        Returns
        -------
        zip obj
            :class:`compas_fea2.model.node.Node`, :class:`compas_fea2.problem.loads.NodeLoad`
        """
        nodes_loads = {}
        for pattern in self.step.patterns:
            if pattern.load_case in self.factors:
                for node, load in pattern.node_load:
                    if node in nodes_loads:
                        nodes_loads[node] += load*self.factors[pattern.load_case]
                    else:
                        nodes_loads[node] = load*self.factors[pattern.load_case]
        return zip(list(nodes_loads.keys()), list(nodes_loads.values()))
