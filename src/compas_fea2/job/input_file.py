from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_fea2 import VERBOSE
from compas_fea2.base import FEAData


class InputFile(FEAData):
    """Input file object for standard FEA.

    Parameters
    ----------
    name : str, optional
        Unique identifier. If not provided, it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Unique identifier.
    problem : :class:`compas_fea2.problem.Problem`
        The problem to generate the input file from.
    model : :class:`compas_fea2.model.Model`
        The model associated with the problem.
    path : str
        Complete path to the input file.

    """

    def __init__(self, problem, **kwargs):
        super(InputFile, self).__init__(**kwargs)
        self._registration = problem
        self._extension = None
        self.path = None

    @property
    def file_name(self):
        return "{}.{}".format(self.problem._name, self._extension)

    @property
    def problem(self):
        return self._registration

    @property
    def model(self):
        return self.problem._registration

    # ==============================================================================
    # General methods
    # ==============================================================================
    def write_to_file(self, path=None):
        """Writes the InputFile to a file in a specified location.

        Parameters
        ----------
        path : str, optional
            Path to the folder where the input file will be saved, by default
            ``None``. If not provided, the Problem path attributed is used.

        Returns
        -------
        str
            Information about the results of the writing process.

        """
        path = path or self.problem.path
        if not path:
            raise ValueError("A path to the folder for the input file must be provided")
        file_path = os.path.join(path, self.file_name)
        with open(file_path, "w") as f:
            f.writelines(self.jobdata())
        if VERBOSE:
            print("Input file generated in the following location: {}".format(file_path))


class ParametersFile(InputFile):
    """"""

    def __init__(self, name=None, **kwargs):
        super(ParametersFile, self).__init__(name, **kwargs)
        raise NotImplementedError()
