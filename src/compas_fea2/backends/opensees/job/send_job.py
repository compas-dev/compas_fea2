
from subprocess import Popen
from subprocess import PIPE

from time import time
from math import sqrt

import json
import os


def launch_process(structure, exe, output):
    """ Runs the analysis through OpenSees.

    Parameters
    ----------
    structure : obj
        Structure object.
    exe : str
        OpenSees exe path to bypass defaults.
    output : bool
        Print terminal output.

    Returns
    -------
    None

    """

    try:

        name = structure.name
        path = structure.path
        temp = '{0}{1}/'.format(path, name)

        try:
            os.stat(temp)
        except:
            os.mkdir(temp)

        tic = time()

        if not exe:
            exe = 'C:/OpenSees.exe'

        command = '{0} {1}{2}.tcl'.format(exe, path, name)
        p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=temp, shell=True)

        print('Executing command ', command)

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

        toc = time() - tic

        print('\n***** OpenSees analysis time : {0} s *****'.format(toc))

    except:

        print('\n***** OpenSees analysis failed')


def launch_optimisation():
    raise NotImplementedError()
