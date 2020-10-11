from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import json

from time import time
from subprocess import Popen
from subprocess import PIPE

from compas_fea2.backends.abaqus.job import odb_extract

# try:
#     from job import *
# except:
#     pass


# Author(s): Andrew Liew (github.com/andrewliew)

__all__ = [
    'extract_data',
]

def extract_data(problem, fields, exe, output, return_data, components):
    """Extract data from the Abaqus .odb file.

    Parameters
    ----------
    structure : obj
        Structure object.
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

    #  Extract

    name = problem.name
    path = problem.path
    temp = path+'/'

    if isinstance(fields, str):
        fields = [fields]

    fields     = ','.join(fields)
    components = ','.join(components) if components else 'None'

    tic1 = time()

    subprocess = 'noGUI={0}'.format(odb_extract.__file__.replace('\\', '/'))

    if not exe:

        args = ['abaqus', 'cae', subprocess, '--', components, fields, name, temp]
        p    = Popen(args, stdout=PIPE, stderr=PIPE, cwd=temp, shell=True)

        while True:

            line = p.stdout.readline()
            if not line:
                break
            line = str(line.strip())

            if output:
                print(line)

        stdout, stderr = p.communicate()

        if output:
            print(stdout)
            print(stderr)

    else:

        os.chdir(temp)
        os.system('{0}{1} -- {2} {3} {4} {5}'.format(exe, subprocess, components, fields, name, temp))

    toc1 = time() - tic1

    if output:
        print('\n***** Data extracted from Abaqus .odb file : {0:.3f} s *****\n'.format(toc1))

    # Save results to Problem

    if return_data:

        try:

            tic2 = time()

            with open('{0}{1}-results.json'.format(temp, name), 'r') as f:
                results = json.load(f)

            with open('{0}{1}-info.json'.format(temp, name), 'r') as f:
                info = json.load(f)

            for step in results:

                for dtype in results[step]:

                    if dtype in ['nodal', 'element']:

                        for field in results[step][dtype]:

                            data = {}

                            for key in results[step][dtype][field]:
                                data[int(key)] = results[step][dtype][field][key]

                            results[step][dtype][field] = data

            problem.results = results

            for step in info:
                problem.results[step]['info'] = info[step]

            toc2 = time() - tic2

            if output:
                print('***** Saving data to structure.results successful : {0:.3f} s *****\n'.format(toc2))

        except:

            if output:
                print('***** Saving data to structure.results unsuccessful *****')


if __name__ == "__main__":
    pass
