from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

<<<<<<< HEAD:src/compas_fea2/job/input_file.py
import os


class InputFile(object):
    """Input file object for standard analysis.

    Parameters
    ----------
    problem : :class:`compas_fea2.problem.Problem`
        Problem object.

    Attributes
    ----------
    job_name : str
        Name of the Abaqus job.
        This is the same as the input file name.

    """
=======

class InputFileBase():
    """Input file object for standard FEA.
    """

    def __init__(self):
        self.__name__ = "Input File"
        self._job_name = None
        self._job_data = None
        self._file_name = None

    @classmethod
    def from_problem(cls, problem):
        """[summary]

        Parameters
        ----------
        problem : obj
            :class:`ProblemBase` sub class object.

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
>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c:src/compas_fea2/_base/job/input_file.py

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self._job_name)

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
<<<<<<< HEAD:src/compas_fea2/job/input_file.py
            filepath = os.path.join(path, self.name)
            with open(filepath, 'w') as f:
                f.writelines(self._jobdata)
            r = '***** {} generated in: {} *****\n'.format(self._input_file_type, filepath)
        except Exception:
            r = '***** ERROR: Input file not generated ****'
=======
            file_path = os.path.join(path, self._file_name)
            with open(file_path, 'w') as f:
                f.writelines(self._job_data)
            r = f'***** {self!r} generated in: {file_path} *****\n'
        except:
            r = f'***** ERROR: {self!r} not generated ****'
>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c:src/compas_fea2/_base/job/input_file.py

        return r
