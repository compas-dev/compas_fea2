from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from subprocess import Popen
from subprocess import PIPE


def launch_process(problem, *, exe, output, overwrite, cpus):
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
    cpus : int
        Number of CPU cores to use.


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

    # if user_mat:
    #     umat_path = problem.materials[user_mat].sub_path
    #     user_sub_kw = 'user={}'.format(umat_path)
    if exe:
        exe_kw = exe

    # Analyse
    success = False
    cmd = 'cd {} && {} {} cpus={} job={} interactive resultsformat=odb {}'.format(
        problem.path, exe_kw, user_sub_kw, cpus, problem.name, overwrite_kw)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=problem.path, shell=True, env=os.environ)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.strip().decode()
        if output:
            print(line)

        if 'COMPLETED' in line:
            success = True

    stdout, stderr = p.communicate()

    if output:
        print(stdout.decode())
        print(stderr.decode())

    if not success:
        try:
            with open(problem.path + problem.name + '.sta', 'r') as f:
                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True
        except Exception:
            pass

    print('***** Analysis {} *****'.format('successful' if success else 'failed'))


# TODO combine with previous
def launch_optimisation(problem, cpus, output):
    """ Run the topology optimisation through Tosca.

    Note
    ----
    https://abaqus-docs.mit.edu/2017/English/TsoUserMap/tso-c-usr-control-start-commandLine.htm
    http://194.167.201.93/English/TsoUserMap/tso-c-usr-control-tp-cmdline.htm#tso-c-usr-control-tp-cmdline

    Parameters
    ----------
    problem : obj
        :class:`OptimisationProblem` subclass object.
    output : bool
        Print terminal output.

    Returns
    -------
    None

    """

    # Set options
    exe_kw = 'ToscaStructure'
    # Analyse
    success = False

    # cmd = f'cd {problem.path} && abaqus optimization task=c:/code/myrepos/from_compas/fea2/temp/topopt_hypar_gmsh/hypar.par job=c:/temp/test_opt interactive'
    cmd = f'cd {problem._path} && {exe_kw} --job {problem._name} -scpus {cpus} --loglevel NOTICE --solver abaqus --ow'
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=problem._path, shell=True, env=os.environ)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.strip().decode()

        if output:
            print(line)

        if 'Application finished successfully' in line:
            success = True

    stdout, stderr = p.communicate()

    if output:
        print(stdout.decode())
        print(stderr.decode())

    if not success:
        try:
            with open(problem.path + problem.name + '.sta', 'r') as f:
                if 'COMPLETED SUCCESSFULLY' in f.readlines()[-1]:
                    success = True
        except Exception:
            pass

    print('***** Analysis {} *****'.format('successful' if success else 'failed'))


def smooth_optimisation(problem, output):
    raise NotImplementedError
