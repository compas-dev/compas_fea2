from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

from time import time
from subprocess import Popen
from subprocess import PIPE

from compas_fea2 import UMAT  #TODO change

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'launch_process',
]

def launch_process(structure, exe, cpus, output, overwrite, user_sub):

    """ Runs the analysis through Abaqus.

    Parameters
    ----------
    structure : obj
        Structure object.
    exe : str
        Abaqus exe path to bypass defaults.
    cpus : int
        Number of CPU cores to use.
    output : bool
        Print terminal output.
    overwrite : bool
        Automatically overwrite results
    user_sub : bool
        Use a user subroutine to run the analysis

    Returns
    -------
    None

    """

    name = structure.name
    path = structure.path
    temp = '{0}{1}/'.format(path, name)

    # Set options
    overwrite_kw=''
    user_sub_kw=''
    exe_kw='abaqus'
    if overwrite:
        overwrite_kw = 'ask_delete=OFF'
    if user_sub:
        # umat_path=os.path.join(UMAT,'umat-hooke-iso.f') #TODO should be like this
        umat_path=os.path.join('C:/Code/COMPAS/compas_fea2/src/compas_fea2/backends/abaqus/components/umat','umat-hooke-iso.f')
        user_sub_kw = 'user={}'.format(umat_path)
    if exe:
        exe_kw = exe

    # Analyse
    tic = time()
    success    = False

    cmd='cd {} && {} {} job={} interactive {}'.format(path,exe_kw, user_sub_kw, name, overwrite_kw)
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

    # success = True
    toc = time() - tic

    if not success:
        try:
            with open(temp + name + '.sta', 'r') as f:
                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True
        except:
            pass

    if success:
        if output:
            print('***** Analysis successful - analysis time : {0} s *****'.format(toc))
    else:
        print('***** Analysis failed *****')



