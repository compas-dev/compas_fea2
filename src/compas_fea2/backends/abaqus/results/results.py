from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
import sys
import json

from time import time
from subprocess import Popen
from subprocess import PIPE

from compas_fea2.backends._base.results import ResultsBase
from compas_fea2.backends._base.results import CaseResultsBase
from compas_fea2.backends.abaqus.job import odb_extract

# Author(s): Francesco Ranaudo (github.com/franaudo)


class Results(ResultsBase):

    def __init__(self, problem, fields, steps='all', sets=None, output=True,
                 components=None, exe=None, license='research',):
        super(Results, self).__init__(problem, fields, steps, sets, components, output)
        self.exe = exe
        self.license = license

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_problem(cls, problem, fields, steps='all', sets=None, output=True, components=None,
                     exe=None, license='research'):
        results = cls(problem, fields, steps, sets, output, components, exe, license)
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
            args = ['abaqus', 'cae', subprocess, '--', components, fields, self.problem_name, temp]
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=temp, shell=True)
            while True:
                # TODO decode line
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
                                                         components, fields, self.problem_name, temp))

        toc1 = time() - tic1
        if self.output:
            print('\n***** Data extracted from Abaqus .odb file : {0:.3f} s *****\n'.format(toc1))

        # Save results back into the Results object
        tic2 = time()

        with open(os.path.join(temp, '{}-results.pkl'.format(self.problem_name)), 'rb') as f:
            results = pickle.load(f)
        for step in results:
            for dtype in results[step]:
                if dtype in ['nodal', 'element']:
                    for field in results[step][dtype]:
                        data = {}
                        for key in results[step][dtype][field]:
                            data[int(key)] = results[step][dtype][field][key]
                        results[step][dtype][field] = data

            self._nodal[step] = results[step]['nodal']
            self._element[step] = results[step]['element']

        with open(os.path.join(temp, '{}-info.pkl'.format(self.problem_name)), 'rb') as f:
            info = pickle.load(f)
        for step in info:
            self._info[step] = info[step]

        toc2 = time() - tic2

        if self.output:
            print('***** Data stored successfully : {0:.3f} s *****\n'.format(toc2))


class StepResults(CaseResultsBase):

    def __init__(self):
        super(Results, self).__init__()


if __name__ == "__main__":
    pass
