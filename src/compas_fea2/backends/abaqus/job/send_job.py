from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

from time import time
from subprocess import Popen
from subprocess import PIPE

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'launch_process',
]

def write_input_file(structure, path):
    pass

def launch_process(structure, path, exe, cpus, output, overwrite, user_mat):

    """ Runs the analysis through Abaqus.

    Parameters
    ----------
    structure : obj
        Structure object.
    path : str
        Path where to start the process.
    exe : str
        Abaqus exe path to bypass defaults.
    cpus : int
        Number of CPU cores to use.
    output : bool
        Print terminal output.
    overwrite : bool
        Automatically overwrite results
    user_mat : str
        Name of the material defined through a subroutine (currently only one material is supported)

    Returns
    -------
    None

    """

    # Set options
    overwrite_kw=''
    user_sub_kw=''
    exe_kw='abaqus'
    if overwrite:
        overwrite_kw = 'ask_delete=OFF'
    if user_mat:
        umat_path = structure.materials[user_mat].sub_path
        user_sub_kw ='user={}'.format(umat_path)
    if exe:
        exe_kw = exe

    # Analyse
    tic = time()
    success    = False
    cmd='cd {} && {} {} job={} interactive {}'.format(path, exe_kw, user_sub_kw, structure.name, overwrite_kw)
    p    = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=path, shell=True)

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
            with open(path + structure.name + '.sta', 'r') as f:
                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True
        except:
            pass

    if success:
        if output:
            print('***** Analysis successful - analysis time : {0} s *****'.format(toc))
    else:
        print('***** Analysis failed *****')



