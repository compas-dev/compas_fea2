from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

# TODO implement __*__ magic method for combination


class Pattern(FEAData):
    """A pattern is the spatial distribution of a specific set of forces,
    displacements, temperatures, and other effects which act on a structure.
    Any combination of nodes and elements may be subjected to loading and
    kinematic conditions.

    Parameters
    ----------
    FEAData : _type_
        _description_
    """

    def __init__(self, load, distribution, name=None, **kwargs):
        super(Pattern, self).__init__(name, **kwargs)
        self._load = load
        self._distribution = distribution

    # def __add__(self, other):
    #     if not isinstance(other, Pattern):
    #         raise NotImplementedError('Sum between a pattern and {!r} is not defined')

    #     for location in self.distribution:
    #         if location in other.distribution:

    #     new_pattern =Pattern()

    @property
    def load(self):
        return self._load

    @property
    def distribution(self):
        return self._distribution
