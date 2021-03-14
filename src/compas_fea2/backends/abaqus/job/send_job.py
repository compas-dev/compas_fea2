from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from time import time
import subprocess
import os
from subprocess import Popen
from subprocess import PIPE

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'launch_process',
]


def launch_process(problem, exe, output, overwrite, user_mat):
    """ Run the analysis through Abaqus.

    Parameters
    ----------
    problem : obj
        problem object.
    exe : str
        Abaqus exe path to bypass defaults.
    output : bool
        Print terminal output.
    overwrite : bool
        Automatically overwrite results
    user_mat : str TODO: REMOVE!
        Name of the material defined through a subroutine (currently only one material is supported)

    Returns
    -------
    None

    """
    # proc = Popen(args, env={'PATH': os.getenv('PATH')})

    # Set options
    overwrite_kw = ''
    user_sub_kw = ''
    exe_kw = 'abaqus'
    if overwrite:
        overwrite_kw = 'ask_delete=OFF'
    if user_mat:
        umat_path = problem.materials[user_mat].sub_path
        user_sub_kw = 'user={}'.format(umat_path)
    if exe:
        exe_kw = exe

    # Analyse
    tic = time()
    success = False
    cmd = 'cd {} && {} {} job={} interactive {}'.format(problem.path, exe_kw, user_sub_kw, problem.name, overwrite_kw)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=problem.path, shell=True, env=os.environ)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = str(line.strip())

        if output:
            print(line)

        if 'COMPLETED' in line:
            success = True

    stdout, stderr = p.communicate()

    if output:
        print(stdout)
        print(stderr)

    toc = time() - tic

    if not success:
        try:
            with open(problem.path + problem.name + '.sta', 'r') as f:
                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True
        except:
            pass

    if success:
        if output:
            print('***** Analysis successful - analysis time : {0} s *****'.format(toc))
    else:
        print('***** Analysis failed *****')


def launch_optimisation(problem, output):
    """ Run the topology optimisation through Tosca.

    Parameters
    ----------
    problem : obj
        Problem object.
    output : bool
        Print terminal output.

    Returns
    -------
    None

    """

    # Set options
    exe_kw = 'ToscaStructure'

    # Analyse
    tic = time()
    success = False
    cmd = 'cd {} && {} --job {} --cpus {}'.format(problem.path, exe_kw, problem.name, problem.cpus)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=problem.path, shell=True)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = str(line.strip())

        if output:
            print(line)

        if 'Application finished successfully' in line:
            success = True

    stdout, stderr = p.communicate()

    if output:
        print(stdout)
        print(stderr)

    toc = time() - tic

    if not success:
        try:
            with open(problem.path + problem.name + '.sta', 'r') as f:
                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True
        except:
            pass

    if success:
        if output:
            print('***** Analysis successful - analysis time : {0} s *****'.format(toc))
    else:
        print('***** Analysis failed *****')
