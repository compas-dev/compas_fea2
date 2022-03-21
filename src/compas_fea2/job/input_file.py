from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
            filepath = os.path.join(path, self.name)
            with open(filepath, 'w') as f:
                f.writelines(self._jobdata)
            r = '***** {} generated in: {} *****\n'.format(self._input_file_type, filepath)
        except Exception:
            r = '***** ERROR: Input file not generated ****'

        return r
