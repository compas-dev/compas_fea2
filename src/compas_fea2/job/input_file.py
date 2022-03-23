from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from compas_fea2.base import FEAData


class InputFile(FEAData):
    """Input file object for standard FEA.
    """

    def __init__(self):
        self._job_name = None
        self._job_data = None
        self._file_name = None

    @classmethod
    def from_problem(cls, problem):
        """Create an InputFile object from a :class:`compas_fea2.problem.Problem`

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            Problem to be converted to InputFile.

        Returns
        -------
        obj
            InputFile for the analysis.
        """
        input_file = cls()
        input_file._job_name = problem._name
        input_file._file_name = f'{problem._name}.{input_file._extension}'
        input_file._job_data = input_file._generate_jobdata(problem)
        return input_file

    # ==============================================================================
    # General methods
    # ==============================================================================

    def write_to_file(self, path):
        """Writes the InputFile to a file in a specified location.

        Parameters
        ----------
        path : str
            Path to the folder where the input file will be saved.

        Returns
        -------
        r : str
            Information about the results of the writing process.
        """

        try:
            file_path = os.path.join(path, self._file_name)
            with open(file_path, 'w') as f:
                f.writelines(self._job_data)
            out = '***** {!r} generated in: {} *****\n'.format(self, file_path)
        except:
            out = '***** ERROR: {!r} not generated ****'.format(self)

        return out
