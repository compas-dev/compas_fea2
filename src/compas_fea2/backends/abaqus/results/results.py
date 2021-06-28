from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

from time import time
from subprocess import Popen
from subprocess import PIPE

from compas_fea2.backends._base.results import ResultsBase
from compas_fea2.backends._base.results import CaseResultsBase
from compas_fea2.backends.abaqus.job import odb_extract

# Author(s): Francesco Ranaudo (github.com/franaudo)


class Results(ResultsBase):

    def __init__(self, database_name, database_path, fields='all', steps='all', sets=None, output=True,
                 components=None, exe=None, license='research',):
        super(Results, self).__init__(database_name, database_path, fields, steps, sets, components, output)
        self.exe = exe
        self.license = license

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_problem(cls, problem, fields='all', steps='all', sets=None, output=True, components=None,
                     exe=None, license='research'):
        results = cls(problem.name, problem.path, fields, steps, sets, output, components, exe, license)
        results.extract_data()
        return results

     # ==========================================================================
    # Extract results
    # ==========================================================================

    def extract_data(self):
        """Extract data from the Abaqus .odb file.

        Parameters
        ----------
        fields : list
            Data field requests.
        exe : str
            Abaqus exe path to bypass defaults.
        output : bool
            Print terminal output.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.

        Returns
        -------
        None

        """

        temp = str(self.database_path)+'/'
        fields = ','.join(self.fields)
        components = ','.join(self.components) if self.components else 'None'

        # TODO create a timer decorator
        tic1 = time()

        subprocess = 'noGUI={0}'.format(odb_extract.__file__.replace('\\', '/'))

        if not self.exe:
            args = ['abaqus', 'cae', subprocess, '--', components, fields, self.database_name, temp]
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=temp, shell=True)
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
            os.chdir(temp)
            os.system('{0}{1} -- {2} {3} {4} {5}'.format(self.exe, subprocess,
                                                         components, fields, self.database_name, temp))

        toc1 = time() - tic1
        if self.output:
            print('\n***** Data extracted from Abaqus .odb file : {0:.3f} s *****\n'.format(toc1))

        # Save results back into the Results object
        tic2 = time()

        for result_type in ['results', 'info']:
            file = os.path.join(temp, '{}-{}.pkl'.format(self.database_name, result_type))
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


class StepResults(CaseResultsBase):

    def __init__(self):
        super(Results, self).__init__()


if __name__ == "__main__":
    pass
