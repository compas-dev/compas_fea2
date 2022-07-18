from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from re import L

from compas_fea2.results import Results, StepResults
from compas_fea2.backends.abaqus.results import odb_extract
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process


class AbaqusResults(Results):
    """Abaqus implementation of :class:`Results`.\n"""
    __doc__ += Results.__doc__

    def __init__(self, database_name, database_path):
        super(AbaqusResults, self).__init__(database_name=database_name, database_path=database_path)

    # ==========================================================================
    # Extract results
    # ==========================================================================
    @timer(message='Data extracted from Abaqus .odb file in')
    def extract_data(self, fields=None):
        """Extract data from the Abaqus .odb file.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Returns
        -------
        None

        """
        import json
        print('\nExtracting data from Abaqus .odb file...')

        args = ['abaqus', 'python', Path(odb_extract.__file__), ','.join(fields) if fields else 'None',
                self.database_path, self.database_name]
        for line in launch_process(cmd_args=args, cwd=self.database_path, output=True):
            print(line)
        return Path(self.database_path).joinpath('{}-results.json'.format(self.database_name))
        print('Data stored successfully in {}'.format(file))


class AbaqusStepResults(StepResults):
    """Abaqus implementation of :class:`StepResults`.\n"""
    __doc__ += StepResults.__doc__

    def __init__(self, step, model):
        super(AbaqusStepResults, self).__init__(step, model)
