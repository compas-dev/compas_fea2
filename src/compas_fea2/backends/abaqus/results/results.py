from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
from pathlib import Path
from time import time
from subprocess import Popen
from subprocess import PIPE

from compas_fea2.results import Results
from compas_fea2.results import CaseResults
from compas_fea2.backends.abaqus.results import odb_extract

# Author(s): Francesco Ranaudo (github.com/franaudo)


class AbaqusResults(Results):

    def __init__(self, database_name, database_path, fields='all', steps='all', sets=None, output=True, components=None, exe=None, license='research',):
        super(AbaqusResults, self).__init__(database_name, database_path, fields, steps, sets, components, output)
        self.exe = exe
        self.license = license

    # ==========================================================================
    # Extract results
    # ==========================================================================

    def extract_data(self):
        """Extract data from the Abaqus .odb file.

        Returns
        -------
        None

        """
        # TODO create a timer decorator
        tic1 = time()

        odb_args = []
        for arg in [self.steps, self.components, self.fields]:
            odb_args.append(','.join(arg if isinstance(arg, list) else [arg]) if arg else 'None')

        subprocess = 'noGUI={0}'.format(Path(odb_extract.__file__))

        if not self.exe:
            args = ['abaqus', 'cae', subprocess, '--', *odb_args, self.database_name, self.database_path]
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=self.database_path, shell=True)
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                line = line.strip().decode()
                if self.output:
                    print(line)
            stdout, stderr = p.communicate()
            if self.output:
                print(stdout.decode())
                print(stderr.decode())
        else:
            raise NotImplementedError("custom abaqus.exe location not implemented")
            # os.chdir(self.database_path)
            # os.system('{0}{1} -- {2} {3} {4} {5}'.format(self.exe, subprocess,
            #                                              odb_args, self.database_name, self.database_path))

        toc1 = time() - tic1
        if self.output:
            print('\n***** Data extracted from Abaqus .odb file : {0:.3f} s *****\n'.format(toc1))

        # Save results back into the Results object
        tic2 = time()
        for result_type in ['results', 'info']:
            file = Path(self.database_path).joinpath('{}-{}.pkl'.format(self.database_name, result_type))
            with open(file, 'rb') as f:
                results = pickle.load(f)
            if result_type == 'results':
                for step in results:
                    for dtype in results[step]:
                        if not hasattr(self, dtype):
                            self.__setattr__(dtype, {})
                        self.__getattribute__(dtype)[step] = {field: {int(
                            k): v for k, v in results[step][dtype][field].items()} for field in results[step][dtype]}
            else:
                if not hasattr(self, result_type):
                    self.__setattr__(result_type, {})
                for step in results:
                    self.__getattribute__(result_type)[step] = results[step]
            os.remove(file)
        toc2 = time() - tic2

        if self.output:
            print('***** Data stored successfully : {0:.3f} s *****\n'.format(toc2))


class AbaqusStepResults(CaseResults):

    def __init__(self):
        super(AbaqusStepResults, self).__init__()
