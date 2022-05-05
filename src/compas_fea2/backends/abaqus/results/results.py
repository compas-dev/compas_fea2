from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
from pathlib import Path
from subprocess import Popen
from subprocess import PIPE

from compas_fea2.results import Results
from compas_fea2.backends.abaqus.results import odb_extract
from compas_fea2.utilities._utils import timer


class AbaqusResults(Results):
    """Abaqus implementation of :class:`Results`.\n"""
    __doc__ += Results.__doc__

    def __init__(self, database_name, database_path, exe=None, license='research',):
        super(AbaqusResults, self).__init__(database_name, database_path)
        self.exe = exe
        self.license = license

    # ==========================================================================
    # Extract results
    # ==========================================================================
    @timer(message='Data extracted from Abaqus .odb file in')
    def _extract_data(self, output=False):
        """Extract data from the Abaqus .odb file.

        Returns
        -------
        None

        """
        print('Extracting data from Abaqus .odb file...')

        subprocess = 'noGUI={0}'.format(Path(odb_extract.__file__))

        if not self.exe:
            args = ['abaqus', 'cae', subprocess, '--', self.database_name, self.database_path]
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=self.database_path, shell=True)
            stdout, stderr = p.communicate()
            # print(stdout.decode())
            # print(stderr.decode())
        else:
            raise NotImplementedError("custom abaqus.exe location not implemented")
            os.chdir(self.database_path)
            os.system('{0}{1} -- {2} {3} {4} {5}'.format(self.exe, subprocess,
                                                         odb_args, self.database_name, self.database_path))

        # # Save results back into the Results object
        # for result_type in ['results', 'info']:
        #     file = Path(self.database_path).joinpath('{}-{}.pkl'.format(self.database_name, result_type))
        #     with open(file, 'rb') as f:
        #         results = pickle.load(f)
        #     if result_type == 'results':
        #         for step in results:
        #             for dtype in results[step]:
        #                 if not hasattr(self, dtype):
        #                     self.__setattr__(dtype, {})
        #                 self.__getattribute__(dtype)[step] = {field: {int(
        #                     k): v for k, v in results[step][dtype][field].items()} for field in results[step][dtype]}
        #     else:
        #         if not hasattr(self, result_type):
        #             self.__setattr__(result_type, {})
        #         for step in results:
        #             self.__getattribute__(result_type)[step] = results[step]
        #     os.remove(file)

        #     print('Data stored successfully in {}'.format(file))
